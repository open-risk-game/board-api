import aiomysql
from aiohttp import web


async def get(request):
    params = request.rel_url.query
    board_id = params['board_id']
    query = f'''
        SELECT owner as player_id, tokens, x, y
        FROM tiles
        WHERE boardid = {board_id}
    '''
    async with request.app['pool'].acquire() as db_conn:
        cursor = await db_conn.cursor(aiomysql.DictCursor)
        await cursor.execute(query)
        result = await cursor.fetchall()
        return web.json_response(result)
