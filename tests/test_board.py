import json
import models.board as board


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
        "boardInfo": {
            "id": 2,
            "description": "Test board",
            "playing": 2,
            "status": "playing",
            "players": [
                {
                    "id": 1,
                    "username": "Billy-Bob",
                    "colour": "#6ed173",
                    "wins": 0,
                    "draws": 0,
                    "losses": 0,
                    },
                {
                    "id": 2,
                    "username": "Zanny-Zaz",
                    "colour": "#fa6511",
                    "wins": 0,
                    "draws": 0,
                    "losses": 0,
                    }
                ]
        },
        "tiles": [
            {
                "id": 10,
                "owner": 1,
                "tokens": 5,
                "x": 0,
                "y": 0,
                "playable": 1,
                "neighbors": [
                    11
                ]
            },
            {
                "id": 11,
                "owner": 2,
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
    del actual["boardInfo"]["created"]
    assert actual == expected


async def test_get_board_info_200(pool):
    board_id = 2
    actual = await board.get_board_information(pool, board_id)
    expected = {
            'description': 'Test board',
            'id': 2,
            'playing': 2
            }
    del actual["created"]
    assert expected == actual


async def test_get_board_info_404(pool):
    board_id = 125125125
    actual = await board.get_board_information(pool, board_id)
    expected = {'Error': 'No board exists with that id'}
    assert expected == actual


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
