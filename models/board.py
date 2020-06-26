import aiomysql
from aiohttp import web


async def get(request):
    params = request.rel_url.query
    board_id = params['board_id']
    print(board_id)
    query = f'''
        SELECT player.username, tile.id, tile.tokens
        FROM tiles as tile
        INNER JOIN players as player ON player.id = tile.owner
        WHERE tile.boardid = {board_id}
    '''
    async with request.app['pool'].acquire() as db_conn:
        cursor = await db_conn.cursor(aiomysql.DictCursor)
        await cursor.execute(query)
        result = await cursor.fetchall()
        return web.json_response(result)
