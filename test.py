import pytest
from fastapi.testclient import TestClient
from bson.objectid import ObjectId
from unittest.mock import patch, MagicMock
from main import app, db
from translate_handler import TranslateHandler


@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        yield client


def test_create_word_success(test_client):
    word_input = {"word": "test", "lang": "en"}
    object_id = ObjectId()
    with patch.object(db, "find_one", return_value=None), patch.object(
        db, "insert_one", return_value=MagicMock(inserted_id=str(object_id))
    ), patch.object(
        TranslateHandler,
        "get_translation_info",
        return_value=[
            ["test", None, None, None, None, None, ["test", "en", "en", True]],
            [
                [[None, None, None, None, None, [["test"]]]],
                "en",
                1,
                "en",
                ["test", "en", "en", True],
            ],
            "en",
            [
                "test",
                [
                    [
                        [
                            "noun",
                            [
                                [
                                    "a procedure intended to establish the quality, performance, or reliability of something, especially before it is taken into widespread use.",
                                    "no sparking was visible during the tests",
                                    True,
                                    None,
                                    None,
                                    [
                                        [
                                            [
                                                ["trial"],
                                                ["experiment"],
                                                ["pilot study"],
                                                ["tryout"],
                                                ["check"],
                                                ["examination"],
                                                ["assessment"],
                                                ["evaluation"],
                                                ["appraisal"],
                                                ["investigation"],
                                                ["inspection"],
                                                ["analysis"],
                                                ["scrutiny"],
                                                ["scrutinization"],
                                                ["study"],
                                                ["probe"],
                                                ["exploration"],
                                                ["screening"],
                                                ["audition"],
                                                ["screen test"],
                                            ]
                                        ],
                                        [[["assay"]], [["technical"]]],
                                    ],
                                ],
                                [
                                    "a movable hearth in a reverberating furnace, used for separating gold or silver from lead.",
                                    None,
                                    None,
                                    None,
                                    [["Metallurgy"]],
                                ],
                                [
                                    "the shell or integument of some invertebrates and protozoans, especially the chalky shell of a foraminiferan or the tough outer layer of a tunicate.",
                                    None,
                                    None,
                                    None,
                                    [["Zoology"]],
                                ],
                            ],
                            None,
                            1,
                        ],
                        [
                            "verb",
                            [
                                [
                                    "take measures to check the quality, performance, or reliability of (something), especially before putting it into widespread use or practice.",
                                    "this range has not been tested on animals",
                                    True,
                                    None,
                                    None,
                                    [
                                        [
                                            [
                                                ["try out"],
                                                ["trial"],
                                                ["carry out trials on"],
                                                ["put to the test"],
                                                ["put through its paces"],
                                                ["experiment with"],
                                                ["pilot"],
                                                ["check"],
                                                ["examine"],
                                                ["assess"],
                                                ["evaluate"],
                                                ["appraise"],
                                                ["investigate"],
                                                ["analyze"],
                                                ["scrutinize"],
                                                ["study"],
                                                ["probe"],
                                                ["explore"],
                                                ["sample"],
                                                ["screen"],
                                            ]
                                        ],
                                        [[["assay"]], [["technical"]]],
                                    ],
                                ]
                            ],
                            None,
                            2,
                        ],
                        [
                            "abbreviation",
                            [["testator.", None, True], ["testimony."], ["Testament."]],
                            None,
                            6,
                        ],
                    ],
                    7,
                    True,
                ],
                [
                    [
                        [None, "such behavior would severely <b>test</b> any marriage"],
                        [None, "a statutory <b>test</b> of obscenity"],
                        [None, "researchers developed a <b>test</b> for the virus"],
                        [None, "a spelling <b>test</b>"],
                        [
                            None,
                            "a useful way to <b>test</b> out ideas before implementation",
                        ],
                        [None, "the exam will <b>test</b> accuracy and neatness"],
                        [None, "a positive <b>test</b> for protein"],
                        [
                            None,
                            "this is the first serious <b>test</b> of the peace agreement",
                        ],
                    ],
                    7,
                    8,
                ],
                None,
                None,
                None,
                "test",
                None,
                "en",
                1,
            ],
        ],
    ):
        response = test_client.post("/translate_word", json=word_input)
        assert response.status_code == 201
        assert response.json() == None


def test_create_word_existing_translation(test_client):
    word_input = {"word": "test", "lang": "en"}
    object_id = ObjectId()
    with patch.object(
        db,
        "find_one",
        return_value={
            "_id": str(object_id),
            "name": "mock_word",
            "translation": "mock_translation",
        },
    ):
        response = test_client.post("/translate_word", json=word_input)
        assert response.status_code == 200
        assert response.json() == {
            "_id": str(object_id),
            "name": "mock_word",
            "translation": "mock_translation",
        }


def test_create_word_not_found(test_client):
    word_input = {"word": "not_found", "lang": "en"}
    with patch.object(db, "find_one", return_value=None), patch.object(
        TranslateHandler, "get_translation_info", return_value=[]
    ):
        response = test_client.post("/translate_word", json=word_input)
        assert response.status_code == 404
        assert response.json() == {
            "detail": "No translation found. Please, check word and language"
        }


def test_show_word(test_client):
    object_id = ObjectId()
    with patch.object(
        db,
        "find",
        return_value=[
            {
                "_id": object_id,
                "lang": "test_lang",
                "synonyms": [],
                "translations": [],
                "examples": [],
                "definitions": [],
                "name": "test_word",
            }
        ],
    ):
        response = test_client.get("/test")
        assert response.status_code == 200
        assert response.json() == [
            {
                "_id": str(object_id),
                "lang": "test_lang",
                "name": "test_word",
                "synonyms": [],
                "translations": [],
                "examples": [],
                "definitions": [],
            }
        ]


def test_delete_word_success(test_client):
    with patch.object(db, "delete_one", return_value=MagicMock(deleted_count=1)):
        response = test_client.delete("/test_word")
        assert response.status_code == 204


def test_delete_word_not_found(test_client):
    with patch.object(db, "delete_one", return_value=MagicMock(deleted_count=0)):
        response = test_client.delete("/not_found")
        assert response.status_code == 404
        assert response.json() == {"detail": "Word not_found not found"}
