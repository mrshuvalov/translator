import re
import random
import json
from urllib.parse import urlencode, quote
from typing import List, Tuple

import requests
from selenium import webdriver

from utils import extract_value


def generate_request_id():
    """Generate a random request ID"""
    return 1000 + int(random.randint(1, 100) * 9000)


class APIRequests:
    """
    A translator that leverages Google Translate's API endpoint.

    Attributes:
    url (str): Google Translate base URL
    """

    url = 'https://translate.google.com'

    def get_google_translate_page(self, word: str, lang: str) -> str:
        """
        Fetches the Google Translate page for the given word and target language.
        
        Args:
        word (str): word or phrase to translate
        target_lang (str): language code of the target language

        Returns:
        str: Google Translate page source
        """
        driver = webdriver.Chrome()
        driver.get(f"{self.url}/?sl=en&tl={lang}&text={word}&op=translate")
        return driver.page_source

    def _get_batch_url(self, page: str) -> str:
        """Extracts batch URL from page source"""
        data = {
            'rpcids': extract_value(page, 'MkEWBc'),
            'f.sid': extract_value(page, 'FdrFJe'),
            'bl': extract_value(page, 'cfb2h'),
            'soc-app': 1,
            'soc-platform': 1,
            'soc-device': 1,
            '_reqid': generate_request_id(),
            'rt': 'c'
        }
        return self.url + '/_/TranslateWebserverUi/data/batchexecute?' + urlencode(data)

    def fetch_translation(self, page: str, word: str, target_lang: str) -> Tuple[str, List[Tuple[str, str]]]:
        """
        Fetches the raw translation object and detected language for the given word and target language.
        
        Args:
        page (str): Google Translate page source
        word (str): word or phrase to translate
        target_lang (str): language code of the target language

        Returns:
        Tuple[str, List[Tuple[str, str]]]: JSON string of the raw translation object and detected language
        """
        batch_url = self._get_batch_url(page)

        payload = 'f.req=' + quote(json.dumps([[['MkEWBc', json.dumps([[word, 'en', target_lang, True], [None]], separators=(',', ':')), None, 'generic']]], separators=(',', ':'))) + '&'
        response = requests.post(batch_url, data=payload, headers={'content-type': 'application/x-www-form-urlencoded;charset=UTF-8'})
        
        # remove garbage prefix
        decoded_res = response.content.decode()[6:]
        # extract length of JSON object
        length = re.search(r'^\d+', decoded_res)[0]
        # extract all JSON object data
        res_all_info = json.loads(decoded_res[len(length):int(length)+len(length)])

        # return raw translation object and detected language
        translation_object = json.loads(res_all_info[0][2])
        
        return translation_object