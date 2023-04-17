from api_requests import APIRequests
from models import WordModel
from utils import get_nested_object

from fastapi import HTTPException


class TranslateHandler:
    """
    Handler to translate a word in a given language.
    """

    def get_translation_info(self, word, lang):
        """
        Get the raw translation object from Google Translate API.
        
        Args:
            word: The word to translate.
            lang: The language code to translate to.
            
        Returns:
            The raw translation object as HTML string.
        """
        api_requests = APIRequests()
        page = api_requests.get_google_translate_page(word=word, lang=lang)
        return api_requests.fetch_translation(page=page, word=word, target_lang=lang)

    def get_translation_obj(self, word, lang):
        """
        Get the WordModel object with translated word information.
        
        Args:
            word: The word to translate.
            lang: The language code to translate to.
            
        Returns:
            The WordModel object with translations, synonyms, definitions, and examples.
            
        Raises:
            Exception: If there is no translation available.
        """
        raw_object = self.get_translation_info(word=word, lang=lang)
        if len(raw_object) < 4:
            return WordModel(name=word, lang=lang, translations=[], synonyms=[], definitions=[], examples=[])

        translations, synonyms = self.set_detailed_translations(raw_object)
        unique_synonyms = list(set(synonyms))
        definitions = self.set_definitions(raw_object)
        examples = self.set_examples(raw_object)
        return WordModel(name=word, lang=lang, translations=translations, synonyms=unique_synonyms, definitions=definitions, examples=examples)
    
    def set_detailed_translations(self, raw_obj):
        """
        Get translated word and synonyms from the raw object.
        
        Args:
            raw_obj: The raw object string.
            
        Returns:
            A tuple of a list of translations and a list of synonyms.
        """
        translations = []
        synonyms = []
        translation_part = get_nested_object(raw_obj, [3, 5, 0])
        if translation_part:
            for translation in translation_part:
                for details in translation[1]:
                    translations.append(details[0])
                    synonyms.extend(details[2])
        return translations, synonyms
    
    def set_definitions(self, raw_obj):
        """
        Get definitions of the word from the raw object.
        
        Args:
            raw_obj: The raw object string.
            
        Returns:
            A list of definitions.
        """
        definitions = []
        definitions_part = get_nested_object(raw_obj, [3, 1, 0])
        if definitions_part:
            for definition_details in definitions_part:
                if len(definition_details) < 2:
                    continue
                for el in definition_details[1]:
                    definitions.append(el[0])
        return definitions

    def set_examples(self, raw_obj):
        """
        Get examples of the word usage from the raw object.
        
        Args:
            raw_obj: The raw object string.
            
        Returns:
            A list of examples.
        """
        examples = []
        examples_part = get_nested_object(raw_obj, [3, 2])
        if examples_part:
            for element in examples_part[0]:
                examples.append(element[1].replace('<b>', '').replace('</b>', ''))
        return examples
