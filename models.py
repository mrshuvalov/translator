from pydantic import BaseModel, Field
from bson.objectid import ObjectId
from typing import Optional, List


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class WordModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    lang: Optional[str] = Field(...)
    name: str = Field(...)
    definitions: List[str] = Field(...)
    synonyms: List[str] = Field(...)
    translations: List[str] = Field(...)
    examples: List[str] = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "challenge",
                "definitions": ["a call to take part in a contest or competition, especially a duel", "an objection or query as to the truth of something, often with an implicit demand for proof"],
                "synonyms": ["Вызов", "Проблема"],
                "translations": ["Испытание"],
                "examples": ["he needed something both to challenge his skills and to regain his crown as the king of the thriller", "I heard the challenge “Who goes there?”"],
            }
        }

class WordInputModel(BaseModel):
    word: str
    lang: Optional[str]
