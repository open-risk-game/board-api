import lib.wincons as wincons


async def test_is_winner():
    board = {
            "boardInfo": {
                "status": "playing",
                "players": [
                    {"id": 34},
                    {"id": 76}
                    ]
                },
            "tiles": [
                {"id": 643, "owner": 34},
                {"id": 654, "owner": 34},
                {"id": 645, "owner": 76},
                ],
            }
    expected = "game-over"
    actual = wincons.domination(board)
    assert expected == actual
