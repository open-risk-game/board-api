import os
import json
import pytest
import aiomysql
import models.board as board

DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_NAME = os.environ.get('DB_NAME')


@pytest.fixture
async def pool(loop):
    async with aiomysql.create_pool(
            host=DB_HOST,
            port=int(DB_PORT),
            user=DB_USER,
            password=DB_PASS,
            db=DB_NAME) as pool:
        yield pool


class FakeURL:

    def __init__(self, queries={}):
        self.query = queries


class FakeRequest:

    def __init__(self, _raise_exception=False, _json=None, app=None, url=None):
        self._json = _json
        self._raise_exception = _raise_exception
        self.app = app or {}
        self.rel_url = url

    async def json(self):
        if self._raise_exception:
            json.loads('None')
        return self._json


async def test_get_board_404(pool):
    fake_url = FakeURL({"id": 2222})
    fake_request = FakeRequest(app={'pool': pool}, url=fake_url)
    response = await board.get_board(fake_request)
    actual = json.loads(response.text)
    expected = {'Error': 'No board exists with that id'}
    assert expected == actual


async def test_get_board_200(pool):
    fake_url = FakeURL({"id": 2})
    fake_request = FakeRequest(app={'pool': pool}, url=fake_url)
    response = await board.get_board(fake_request)
    expected = {
        "board-info": {
            "id": 2,
            "description": "Test board",
            "created": "2020-07-19 21:33:27",
            "playing": 2
        },
        "hexagons": [
            {
                "hex_id": 10,
                "player_id": 1,
                "tokens": 5,
                "x": 0,
                "y": 0,
                "playable": 1,
                "neighbors": [
                    11
                ]
            },
            {
                "hex_id": 11,
                "player_id": 2,
                "tokens": 9,
                "x": 0,
                "y": 1,
                "playable": 1,
                "neighbors": [
                    10
                ]
            }
        ]
    }

    actual = json.loads(response.text)
    assert actual == expected


async def test_get_current_turn(pool):
    url = FakeURL({"id": 2})
    request = FakeRequest(app={'pool': pool}, url=url)
    response = await board.get_turn(request)
    actual = json.loads(response.text)
    expected = {"playing": 2}
    assert expected == actual


async def test_update_current_turn(pool):
    data = {"id": 2, "next": 2}
    request = FakeRequest(app={'pool': pool}, _json=data)
    response = await board.update_turn(request)
    actual = json.loads(response.text)
    expected = {"next-player": 2}
    assert expected == actual
