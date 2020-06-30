import aiomysql
from aiohttp import web
import json


async def hex_edges(app, hex_id):

    query = f'SELECT hex_to FROM edge WHERE hex_from = {hex_id}'
    async with app['pool'].acquire() as db_conn:
        cursor = await db_conn.cursor(aiomysql.DictCursor)
        await cursor.execute(query)
        result = await cursor.fetchall()
        edges = []
        for item in result:
            edges.append(item.get('hex_to'))
        return edges


async def get(request):
    params = request.rel_url.query
    board_id = params['board_id']
    query = f'''
        SELECT id AS hex_id, owner AS player_id, tokens, x, y, playable
        FROM hex
        WHERE boardid = {board_id}
    '''
    async with request.app['pool'].acquire() as db_conn:
        cursor = await db_conn.cursor(aiomysql.DictCursor)
        await cursor.execute(query)
        result = await cursor.fetchall()
        for hexagon in result:
            edges = await hex_edges(request.app, hexagon.get('hex_id'))
            hexagon['neighbors'] = edges
            hexagons = hexagon
        hexagons = json.dumps(hexagons)
        return web.json_response(result)
