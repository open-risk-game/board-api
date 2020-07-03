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
