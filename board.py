import logging
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


class Territory:

    def __init__(self, name, tokens, boarders={}):
        self.name = name
        self.tokens = tokens
        self.boarders = boarders

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
            if result is not None:
                logging.info(f'{result}: Found and returned')
                return web.json_response(result, status=200)
            else:
                message = {
                        'error': f'territory with id {territory_id} not found'
                        }
                logging.info(f'{message}')
                return web.json_response(message, status=404)

    async def get_boarders(request):
        params = request.rel_url.query
        territory_id = params['territory_id']
        query = f'''
        SELECT t.name, t.tokens, t.owner
        FROM territories AS t
        INNER JOIN boarders AS b ON t.id = b.id
        WHERE {territory_id} = b.territory_from_id
        '''
        async with request.app['pool'].acquire() as db_conn:
            cursor = await db_conn.cursor(aiomysql.DictCursor)
            await cursor.execute(query)
            result = await cursor.fetchall()
        return web.json_response({'boarders': result})

    async def add_tokens(request):
        data = await request.json()
        tokens = data.get('tokens')
        territory_id = data.get('territory_id')

        query = f'''
        UPDATE territories
        SET tokens = tokens + {tokens}
        WHERE id = {territory_id}
        '''

        async with request.app['pool'].acquire() as db_conn:
            cursor = await db_conn.cursor(aiomysql.DictCursor)
            await cursor.execute(query)
            result = cursor.rowcount
            if result == -1:
                message = {
                        'error': f'territory with id {territory_id} not found'
                        }
                return web.json_response(message, status=404)
            await db_conn.commit()
            message = {
                    'result': f'updated territory-id {territory_id}'
                    }
            return web.json_response(message, status=200)

    async def change_ownership(request):
        data = await request.json()
        player_id = data.get('player_id')
        territory_id = data.get('territory_id')

        query = f'''
        UPDATE territories
        SET owner = {player_id}
        WHERE id = {territory_id}
        '''
        async with request.app['pool'].acquire() as db_conn:
            cursor = await db_conn.cursor(aiomysql.DictCursor)
            await cursor.execute(query)
            result = cursor.rowcount
            if result == -1:
                message = {
                        'error': f'territory with id {territory_id} not found'
                        }
                return web.json_response(message, status=404)
            await db_conn.commit()
            message = {
                    'result': f'updated territory-id {territory_id}'
                    }
            return web.json_response(message, status=200)
