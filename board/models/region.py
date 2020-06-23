import aiomysql
from aiohttp import web


class Region:

    def __init__(self, name, region={}):
        self.name = name
        self.region = region

    async def get(request):
        region_id = 1
        query = f'''
        SELECT regions.name
        FROM regions
        WHERE id = {region_id}
        '''

        async with request.app['pool'].acquire() as db_conn:
            cursor = await db_conn.cursor(aiomysql.DictCursor)
            await cursor.execute(query)
            result = await cursor.fetchone()

        return web.json_response(result, status=200)
