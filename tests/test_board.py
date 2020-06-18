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


class FakeRequest:

    def __init__(self, _raise_exception=False, _json=None, app=None):
        self._json = _json
        self._raise_exception = _raise_exception
        self.app = app or {}

    async def json(self):
        if self._raise_exception:
            json.loads('None')
        return self._json


async def test_territory_get_200(pool):
    fake_request = FakeRequest(app={'pool': pool})
    response = await Territory.get(fake_request)
    expected = {
              'result': {
                  'name': 'United Kingdom',
                  'owner': 'Red',
                  'region_id': 1,
                  'tokens': 11
                  }
         }

    actual = json.loads(response.text).get('territory')
    assert actual == expected


async def test_region_get_200(pool):
    fake_request = FakeRequest(app={'pool': pool})
    response = await Region.get(fake_request)
    expected = {}

    actual = json.loads(response.text).get('data')
    assert actual == expected
