import os
import json
import pytest
import aiomysql
from board import Territory, Region


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

    def __init__(self, territory_id):
        self.query = {'territory_id': territory_id}


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


def test_is_boardering():
    boarders = [{'id': 4}, {'id': 3}]
    source = Territory(2, 'abc', 11, boarders)
    destination = Territory(3, 'efg', 22)
    actual = Territory.is_boardering(source, destination)
    expected = True
    assert expected == actual


async def test_territory_get_200(pool):
    fake_url = FakeURL(1)
    fake_request = FakeRequest(app={'pool': pool}, url=fake_url)
    response = await Territory.get(fake_request)
    expected = {
              'name': 'Islington',
              'owner': None,
              'region_id': 1,
              'tokens': 11
         }
    actual = json.loads(response.text)
    assert actual == expected


async def test_region_get_200(pool):
    fake_url = FakeURL(1)
    fake_request = FakeRequest(app={'pool': pool}, url=fake_url)
    response = await Region.get(fake_request)
    expected = {
              'name': 'London'
         }
    actual = json.loads(response.text)
    assert actual == expected
