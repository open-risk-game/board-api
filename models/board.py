import aiomysql
from aiohttp import web
from models.tile import tile_edges
from lib.wincons import domination


async def get_tiles(pool, board_id):
    query = '''
        SELECT id, owner, tokens, x, y, playable
        FROM hex
        WHERE boardid = %s
    '''
    async with pool.acquire() as db_conn:
        cursor = await db_conn.cursor(aiomysql.DictCursor)
        await cursor.execute(query, (board_id,))
        result = await cursor.fetchall()
        db_conn.close()
    return result


async def get_players(pool, board_id):
    query = '''
        SELECT player.id, username, colour, wins, draws, losses
        FROM player
        INNER JOIN game ON
            game.player_id = player.id
            AND game.board_id = %s
    '''
    async with pool.acquire() as db_conn:
        cursor = await db_conn.cursor(aiomysql.DictCursor)
        await cursor.execute(query, (board_id,))
        result = await cursor.fetchall()
        db_conn.close()
    return result


async def get_board(request):
    pool = request.app['pool']
    params = request.rel_url.query
    board_id = params['id']
    board_info = await get_board_information(pool, board_id)
    if board_info.get("Error"):
        return web.json_response(board_info)
    players = await get_players(pool, board_id)
    tiles = await get_tiles(
            pool,
            board_id
            )
    board = await build_board_response(
            pool,
            board_info,
            tiles,
            players
            )
    return web.json_response(board)


async def build_board_response(pool, board_info, tiles, players):
    board = {}
    board["boardInfo"] = board_info
    board["boardInfo"]["status"] = domination(players, tiles)
    board["boardInfo"]["players"] = players
    for tile in tiles:
        tile_id = tile.get('id')
        neighbors = await tile_edges(pool, tile_id)
        tile["neighbors"] = neighbors
    board["tiles"] = tiles
    return board


async def get_board_information(pool, board_id):
    query = '''
        SELECT id, description, created, playing
        FROM board
        WHERE id = %s
    '''
    async with pool.acquire() as db_conn:
        cursor = await db_conn.cursor(aiomysql.DictCursor)
        await cursor.execute(query, (board_id,))
        if cursor.rowcount == 0:
            result = {'Error': 'No board exists with that id'}
            db_conn.close()
            return result
        result = await cursor.fetchone()
        result['created'] = str(result.get('created'))
        db_conn.close()
    return result


async def get_turn(request):
    params = request.rel_url.query
    board_id = params['id']
    query = f'SELECT playing FROM board WHERE id = {board_id}'
    async with request.app['pool'].acquire() as db_conn:
        cursor = await db_conn.cursor(aiomysql.DictCursor)
        await cursor.execute(query)
        result = await cursor.fetchone()
    return web.json_response(result, status=200)


async def update_turn(request):
    data = await request.json()
    board_id = data.get('id')
    playing_next = data.get('next')
    query = f'UPDATE board SET playing = {playing_next} WHERE id = {board_id}'
    async with request.app['pool'].acquire() as db_conn:
        cursor = await db_conn.cursor(aiomysql.DictCursor)
        await cursor.execute(query)
        updated = cursor.rownumber
        if updated is not None:
            await db_conn.commit()
            return web.json_response({'next-player': playing_next}, status=200)
        return web.json_response({'next-player': 'None'}, status=404)


async def create(request):
    """
        Create new board on board table.
        Insert player into game table with the new board id.
        Create new tiles for the new board
        Select all the new tiles
        Create edges between the new tiles
    """
    data = await request.json()
    player_id = data.get('playerID')

    async with request.app['pool'].acquire() as db_conn:
        board_query = "INSERT INTO board (playing) VALUES (%s)"
        cursor = await db_conn.cursor()
        await cursor.execute(board_query, (player_id))
        board_id = cursor.lastrowid
        await db_conn.commit()
        db_conn.close()

    async with request.app['pool'].acquire() as db_conn:
        game_query = "INSERT INTO game (player_id, board_id) VALUES (%s, %s)"
        cursor = await db_conn.cursor()
        await cursor.execute(game_query, (player_id, board_id))
        await db_conn.commit()
        db_conn.close()

    async with request.app['pool'].acquire() as db_conn:
        tiles_data = [
                (1, 0, 0, board_id),  # first row
                (player_id, 5, 1, board_id),  # first row
                (1, 0, 1, board_id),  # first row
                (1, 0, 1, board_id),  # second row
                (1, 0, 1, board_id),  # second row
                (1, 0, 1, board_id),  # second row
                (1, 0, 0, board_id),  # third row
                (1, 0, 1, board_id),  # third row
                (1, 0, 1, board_id),  # third row
            ]
        tiles_query = """
            INSERT INTO hex (owner, tokens, playable, boardid)
            VALUES (%s, %s, %s, %s)"""
        cursor = await db_conn.cursor()
        await cursor.executemany(tiles_query, tiles_data)
        await db_conn.commit()
        db_conn.close()

    async with request.app['pool'].acquire() as db_conn:
        new_tiles_query = "SELECT * FROM hex WHERE boardid = %s"
        cursor = await db_conn.cursor()
        await cursor.execute(new_tiles_query, (board_id))
        result = await cursor.fetchall()
        db_conn.close()

    async with request.app['pool'].acquire() as db_conn:
        edges_data = [
                (result[1][0], result[2][0]),
                (result[1][0], result[3][0]),
                (result[1][0], result[4][0]),
                (result[2][0], result[1][0]),
                (result[2][0], result[4][0]),
                (result[2][0], result[5][0]),
                (result[3][0], result[1][0]),
                (result[3][0], result[4][0]),
                (result[3][0], result[7][0]),
                (result[4][0], result[1][0]),
                (result[4][0], result[2][0]),
                (result[4][0], result[3][0]),
                (result[4][0], result[5][0]),
                (result[4][0], result[7][0]),
                (result[4][0], result[8][0]),
                (result[5][0], result[2][0]),
                (result[5][0], result[4][0]),
                (result[5][0], result[8][0]),
                (result[7][0], result[3][0]),
                (result[7][0], result[4][0]),
                (result[7][0], result[8][0]),
                (result[8][0], result[4][0]),
                (result[8][0], result[5][0]),
                (result[8][0], result[7][0]),
            ]
        edges_query = """
            INSERT INTO edge (hex_from, hex_to)
            VALUES (%s, %s)"""
        cursor = await db_conn.cursor()
        await cursor.executemany(edges_query, edges_data)
        await db_conn.commit()
        db_conn.close()

    return web.json_response({"boardID": board_id})
