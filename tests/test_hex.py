import os
import json
import pytest
import aiomysql
import models.hexagon as hexagon

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


async def test_is_connected(pool):
    connected_url = FakeURL(queries={
        "from": '5',
        "to": '2'
        })
    request = FakeRequest(app={'pool': pool}, url=connected_url)
    connected_response = await hexagon.is_connected(request)
    connected_actual = json.loads(connected_response.text)
    assert {"Connection": True} == connected_actual

    not_connected_url = FakeURL(queries={
        "from": 5,
        "to": 2
        })
    not_connected_request = FakeRequest(
            app={'pool': pool},
            url=not_connected_url
            )
    not_connected_response = await hexagon.is_connected(not_connected_request)
    not_connected_actual = json.loads(not_connected_response.text)
    assert {"Connection": True} == not_connected_actual


async def test_get_edges(pool):
    hex_id = 5
    edges = await hexagon.hex_edges(pool, hex_id)
    assert edges == [2, 3, 4, 6, 8, 9]


async def test_get_hex(pool):
    connected_url = FakeURL(
            queries={
                "id": 2
                })
    request = FakeRequest(app={'pool': pool}, url=connected_url)
    response = await hexagon.get_hex(request)
    actual = json.loads(response.text)
    expected = {
            "hex_id": 2,
            "player_id": 1,
            "tokens": 5,
            "x": 0,
            "y": 1,
            "playable": 1,
            "edges": [3, 4, 5]
            }
    assert expected == actual


async def test_change_ownership(pool):
    data = {
            "tokens": 500,
            "hex_id": 1
            }
    request = FakeRequest(app={"pool": pool}, _json=data)
    response = await hexagon.update_tokens(request)
    actual = json.loads(response.text)
    expected = {'result': 'updated hexagon-id 1'}
    assert expected == actual
