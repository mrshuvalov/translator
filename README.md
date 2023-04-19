# translator
Translator app

Microservice providing an API to work with word definitions/translations taken from Google Translate.

# Endpoints

POST /translate_word :
  Receives a word and lang in a JSON object as a POST request and translates it to the language provided in the lang field using the Google Cloud Translate API. If the word is already in the database, then it retrieves the translation from the collection "words". Otherwise, stores the translation to the "words" collection and returns a JSON object with the translation.

GET /{word} :
  Receives a string value as a path parameter and returns a list of all words in the "words" collection that contains the specified value.

DELETE /{word} :
  Receives a word as a path parameter and uses the "words" collection to delete the word from the database if exists. The endpoint returns a message confirming the successful deletion of the word.
  
TODO:
1. Get language codes from google page
2. Create tests to test page parsing logic 

