import os
import json
import pytest
import aiomysql
from models.region import Region
from models.territory import Territory
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

    def __init__(self, board_id):
        self.query = {'board_id': board_id}


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


async def test_get_edges(pool):
    app = {'pool': pool}
    edges = await board.hex_edges(app, 5)
    assert edges == [2, 3, 4, 6, 8, 9]


# async def test_territory_get_200(pool):
#     fake_url = FakeURL(1)
#     fake_request = FakeRequest(app={'pool': pool}, url=fake_url)
#     response = await board.get(fake_request)
#     expected = "[{'hex_id': 1,\n  'neighbors': [],\n  'playable': 0,\n  'player_id': None,\n  'tokens': 0,\n  'x': 0,\n  'y': 0},\n {'hex_id': 2,\n  'neighbors': [3, 4, 5],\n  'playable': 1,\n  'player_id': 1,\n  'tokens': 5,\n  'x': 0,\n  'y': 1},\n {'hex_id': 3,\n  'neighbors': [2, 5, 6],\n  'playable': 1,\n  'player_id': None,\n  'tokens': 0,\n  'x': 0,\n  'y': 1},\n {'hex_id': 4,\n  'neighbors': [2, 5, 8],\n  'playable': 1,\n  'player_id': None,\n  'tokens': 0,\n  'x': 1,\n  'y': 0},\n {'hex_id': 5,\n  'neighbors': [2, 3, 4, 6, 8, 9],\n  'playable': 1,\n  'player_id': None,\n  'tokens': 0,\n  'x': 1,\n  'y': 1},\n {'hex_id': 6,\n  'neighbors': [3, 5, 9],\n  'playable': 1,\n  'player_id': None,\n  'tokens': 0,\n  'x': 1,\n  'y': 2},\n {'hex_id': 7,\n  'neighbors': [],\n  'playable': 0,\n  'player_id': None,\n  'tokens': 0,\n  'x': 2,\n  'y': 0},\n {'hex_id': 8,\n  'neighbors': [4, 5, 9],\n  'playable': 1,\n  'player_id': None,\n  'tokens': 0,\n  'x': 2,\n  'y': 1},\n {'hex_id': 9,\n  'neighbors': [5, 6, 8],\n  'playable': 1,\n  'player_id': 2,\n  'tokens': 7,\n  'x': 2,\n  'y': 2}]"
#     actual = json.loads(response.text)
#     assert actual == expected
# def test_is_boardering():
#     boarders = [{'id': 4}, {'id': 3}]
#     source = Territory(2, 'abc', 11, boarders)
#     destination = Territory(3, 'efg', 22)
#     actual = Territory.is_boardering(source, destination)
#     expected = True
#     assert expected == actual
#
#
# async def test_territory_get_200(pool):
#     fake_url = FakeURL(1)
#     fake_request = FakeRequest(app={'pool': pool}, url=fake_url)
#     response = await Territory.get(fake_request)
#     expected = {
#               'name': 'Islington',
#               'owner': None,
#               'region_id': 1,
#               'tokens': 11
#          }
#     actual = json.loads(response.text)
#     assert actual == expected
#
#
# async def test_region_get_200(pool):
#     fake_url = FakeURL(1)
#     fake_request = FakeRequest(app={'pool': pool}, url=fake_url)
#     response = await Region.get(fake_request)
#     expected = {
#               'name': 'London'
#          }
#     actual = json.loads(response.text)
#     assert actual == expected
