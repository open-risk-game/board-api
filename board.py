import aiomysql
from aiohttp import web


class Region:

    def __init__(self, name, region={}):
        self.name = name
        self.region = region

    async def get(request):
        region_id = 1
        query = f'''
        SELECT territories.name, territories.tokens, territories.owner
        FROM territories
        INNER JOIN regions ON regions.id = territories.region_id
        WHERE territories.region_id = {region_id}
        '''

        async with request.app['pool'].acquire() as db_conn:
            cursor = await db_conn.cursor(aiomysql.DictCursor)
            await cursor.execute(query)
            result = await cursor.fetchall()
            data = {'result': result}

        return web.json_response({'data': data})


class Territory:

    def __init__(self, name, tokens):
        self.name = name
        self.tokens = tokens

    async def get(request):
        params = request.rel_url.query
        territory_id = params['territory_id']
        query = f'''
        SELECT name, tokens, owner, region_id
        FROM territories
        WHERE id = {territory_id}
        '''

        async with request.app['pool'].acquire() as db_conn:
            cursor = await db_conn.cursor(aiomysql.DictCursor)
            await cursor.execute(query)
            result = await cursor.fetchone()

        return web.json_response(result)
