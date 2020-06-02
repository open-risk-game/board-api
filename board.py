import aiomysql
from aiohttp import web


class Region:

    def __init__(self, name, region={}):
        self.name = name
        self.region = region

    async def get(request):
        query = '''
        SELECT territories.name, territories.tokens, territories.owner
        FROM territories
        INNER JOIN regions ON regions.id = territories.region_id
        '''
        async with request.app['pool'].acquire() as db_conn:
            cursor = await db_conn.cursor(aiomysql.DictCursor)
            await cursor.execute(query)
            result = await cursor.fetchone()
            data = {'result': result}

        return web.json_response({'data': data})


class Territory:

    def __init__(self, name, tokens):
        self.name = name
        self.tokens = tokens
