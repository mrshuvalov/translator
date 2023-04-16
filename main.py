import logging
from typing import List, Optional

from fastapi import FastAPI, HTTPException, status, Body
from fastapi.responses import Response, JSONResponse
from fastapi.encoders import jsonable_encoder
import motor.motor_asyncio

from translate_handler import TranslateHandler
from models import WordInputModel, WordModel


Log_Format = '%(asctime)s %(levelname)-8s %(name)-17s %(message)s'
logging.basicConfig(filename='app.log', level=logging.DEBUG, format=Log_Format)

MONGO_DETAILS = "mongodb://admin:admin@mongo:27017"

app = FastAPI()
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
db = client.vacabulary

@app.post("/translate_word", response_description="Translate word", response_model=WordModel)
async def create_word(word: WordInputModel = Body(...)):
    '''
    Translates a word and saves it to the Mongo database words collection
    
    word : str
        The word to be translated
        
    Returns
    -------
    json:
        A JSON object containing the word and its translation
    '''
    logging.debug(f'Creating new word {word.word} in language {word.lang}')
    translation = await db["words"].find_one({"name": word.word, "lang": word.lang})
    if translation:
        logging.debug(f'Translation for word ({word.word}) and language ({word.lang}) is found in the database.')
        return JSONResponse(status_code=status.HTTP_200_OK, content=translation)
    translator = TranslateHandler()
    res = translator.get_translation_obj(word=word.word, lang=word.lang)
    new_word = await db["words"].insert_one(jsonable_encoder(res))
    created_word = await db["words"].find_one({"_id": new_word.inserted_id})
    logging.debug(f'New word successfully created with ID: {new_word.inserted_id}')
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_word)



@app.get(
    "/{word}", response_description="Get words by string", response_model=List[WordModel]
)
async def show_word(word: Optional[str]):
    '''
    Finds words containing the specified string value in the database
    
    word : str
        The string value to search for
        
    Returns
    -------
    list:
        A list of dictionaries representing words containing the specified string value
    '''
    if (word := await db["words"].find({"name": {"$regex": f".*{word}.*"}}).to_list(None)):
        logging.debug(f'Words for string value ({word}) successfully retrieved')
        return word

    raise HTTPException(status_code=404, detail=f"Word {word} not found")



@app.delete("/{word}", response_description="Delete a word")
async def delete_word(word: str):
    '''
    Deletes a word from the database
    
    word : str
        The word to be deleted
        
    Returns
    -------
    str:
        A message confrming that the word has been deleted
    '''
    logging.debug(f'Need to delete: {word}')
    delete_result = await db["words"].delete_one({"_name": word})

    if delete_result.deleted_count == 1:
        logging.debug(f'Word {word} was successfully deleted')
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Word {word} not found")
