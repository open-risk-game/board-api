import aiomysql
from aiohttp import web
import models.hexagon as hexagon


async def get_board(request):
    params = request.rel_url.query
    board_id = params['id']
    query = f'''
        SELECT id AS hex_id, owner AS player_id, tokens, x, y, playable
        FROM hex
        WHERE boardid = {board_id}
    '''
    async with request.app['pool'].acquire() as db_conn:
        cursor = await db_conn.cursor(aiomysql.DictCursor)
        await cursor.execute(query)
        result = await cursor.fetchall()
        for hex_item in result:
            edges = await hexagon.hex_edges(
                    request.app,
                    hex_item.get('hex_id')
                    )
            hex_item['neighbors'] = edges
        return web.json_response(result)


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
        return web.json_response({"board_id": board_id})

