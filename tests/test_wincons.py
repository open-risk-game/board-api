import lib.wincons as wincons


async def test_is_winner():
    players = [{"id": 34}, {"id": 76}]
    tiles = [
            {"id": 643, "owner": 34},
            {"id": 654, "owner": 34},
            {"id": 645, "owner": 76}
            ]
    expected = "playing"
    actual = wincons.domination(players, tiles)
    assert expected == actual
    tiles[2]["owner"] = 34
    expected = "game-over"
    actual = wincons.domination(players, tiles)
    assert expected == actual
