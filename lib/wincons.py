def domination(players, tiles):
    '''
        If any player owns zero tiles they have lost the game

        Bucket search for player that ownes zero tiles
    '''
    status = "playing"
    bucket = {}
    for player in players:
        bucket[player['id']] = 0
    for tile in tiles:
        if tile["owner"] in bucket:
            bucket[tile["owner"]] = bucket[tile["owner"]] + 1
    for player in bucket:
        if bucket[player] == 0:
            status = "game-over"
    return status
