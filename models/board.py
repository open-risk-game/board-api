import json
import aiomysql
import models.tile
from aiohttp import web


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


async def get_board(request):
    pool = request.app['pool']
    params = request.rel_url.query
    board_id = params['id']
    board_info = await get_board_information(pool, board_id)
    if board_info.get('Error'):
        return web.json_response(board_info, status=404)
    tiles = await get_tiles(pool, board_id)
    for tile in tiles:
        neighbors = await models.tile.tile_edges(
                pool,
                tile.get('id')
                )
        tile['neighbors'] = neighbors
    output = {
            'boardInfo': board_info,
            'tiles': tiles
            }
    return web.json_response(output)


async def test(request):
    pool = request.app['pool']
    params = request.rel_url.query
    board_id = params['id']
    board_info = await get_board_information(pool, board_id)
    tiles = await get_tiles(pool, board_id)
    board = build_board_response(pool, board_info, tiles)
    return web.json_response(board)


async def build_board_response(pool, board_info, tiles):
    for tile in tiles:
        tile_id = tile.get('id')
        neighbors = await get_tiles(pool, tile_id)
        tile["neighbors"] = neighbors
    board = {
            "boardInfo": board_info,
            "tiles": tiles
            }
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


async def create_board(request):
    data = await request.json()
    player_A_id = data.get('a')
    player_B_id = data.get('b')
    query = f'''
        INSERT INTO board (playerAid, playerBid)
        VALUES ({player_A_id}, {player_B_id})
    '''
    async with request.app['pool'].acquire() as db_conn:
        cursor = await db_conn.cursor()
        await cursor.execute(query)
        if cursor.lastrowid is None:
            return web.json_response({"error": "Check player IDs"})
        await db_conn.commit()
        board_id = cursor.lastrowid
        return web.json_response({"boardID": board_id})
