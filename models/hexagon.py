import aiomysql
from aiohttp import web


async def is_connected(request):
    params = request.rel_url.query
    hex_from_id = params['from']
    hex_to_id = params['to']
    if int(hex_to_id) in await hex_edges(request.app, int(hex_from_id)):
        return web.json_response({"Connection": True})
    return web.json_response({"Connection": False})


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


async def get_hex(request):
    params = request.rel_url.query
    hex_id = params['id']
    query = f'''
        SELECT id AS hex_id, owner AS player_id, tokens, x, y, playable
        FROM hex
        WHERE id = {hex_id}
    '''
    async with request.app['pool'].acquire() as db_conn:
        cursor = await db_conn.cursor(aiomysql.DictCursor)
        await cursor.execute(query)
        result = await cursor.fetchone()
        if result is not None:
            result['edges'] = await hex_edges(request.app, hex_id)
            return web.json_response(result, status=200)
        else:
            message = {
                    'error': f'Hexagon with id {hex_id} not found'
                    }
            return web.json_response(message, status=404)


async def change_ownership(request):
    data = await request.json()
    player_id = data.get('player_id')
    hex_id = data.get('hex_id')
    query = f'''
        UPDATE hex
        SET owner = {player_id}
        WHERE id = {hex_id}
    '''
    async with request.app['pool'].acquire() as db_conn:
        cursor = await db_conn.cursor(aiomysql.DictCursor)
        await cursor.execute(query)
        result = cursor.rowcount
        if result == -1:
            message = {
                    'error': f'hex with id {hex_id} not found'
                    }
            return web.json_response(message, status=404)
        await db_conn.commit()
        message = {
                'result': f'updated hex-id {hex_id}'
                }
        return web.json_response(message, status=200)


async def update_tokens(request):
    data = await request.json()
    tokens = data.get('tokens')
    hex_id = data.get('hex_id')

    query = f'''
    UPDATE hex
    SET tokens = tokens + {tokens}
    WHERE id = {hex_id}
    '''

    async with request.app['pool'].acquire() as db_conn:
        cursor = await db_conn.cursor(aiomysql.DictCursor)
        await cursor.execute(query)
        result = cursor.rowcount
        if result == -1:
            message = {
                    'error': f'hexagon with id {hex_id} not found'
                    }
            return web.json_response(message, status=404)
        await db_conn.commit()
        message = {
                'result': f'updated hexagon-id {hex_id}'
                }
        return web.json_response(message, status=200)
