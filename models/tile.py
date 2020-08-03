import aiomysql
from aiohttp import web


async def is_connected(request):
    params = request.rel_url.query
    tile_from_id = params['from']
    tile_to_id = params['to']
    pool = request.app['pool']
    if int(tile_to_id) in await tile_edges(pool, int(tile_from_id)):
        return web.json_response({"Connection": True})
    return web.json_response({"Connection": False})


async def tile_edges(pool, tile_id):
    query = f'SELECT hex_to FROM edge WHERE hex_from = {tile_id}'
    async with pool.acquire() as db_conn:
        cursor = await db_conn.cursor(aiomysql.DictCursor)
        await cursor.execute(query)
        result = await cursor.fetchall()
        edges = []
        for item in result:
            edges.append(item.get('hex_to'))
        db_conn.close()
    return edges


async def get_tile(request):
    params = request.rel_url.query
    tile_id = params['id']
    query = f'''
        SELECT id, owner, tokens, x, y, playable
        FROM hex
        WHERE id = {tile_id}
    '''
    pool = request.app['pool']
    async with pool.acquire() as db_conn:
        cursor = await db_conn.cursor(aiomysql.DictCursor)
        await cursor.execute(query)
        result = await cursor.fetchone()
        if result is not None:
            result['edges'] = await tile_edges(pool, tile_id)
            status = 200
        else:
            result = {
                    'error': f'Hexagon with id {tile_id} not found'
                   }
        db_conn.close()
    return web.json_response(result, status=status)


async def change_ownership(request):
    data = await request.json()
    player_id = data.get('player_id')
    tile_id = data.get('tile_id')
    query = f'''
        UPDATE hex
        SET owner = {player_id}
        WHERE id = {tile_id}
    '''
    async with request.app['pool'].acquire() as db_conn:
        cursor = await db_conn.cursor(aiomysql.DictCursor)
        await cursor.execute(query)
        result = cursor.rowcount
        if result == -1:
            message = {
                    'Error': f'Tile with id {tile_id} not found'
                    }
            return web.json_response(message, status=404)
        await db_conn.commit()
        message = {
                'Result': f'Updated tile-id {tile_id}'
                }
        return web.json_response(message, status=200)


async def update_tokens(request):
    data = await request.json()
    tokens = data.get('tokens')
    tile_id = data.get('tile_id')

    query = f'''
    UPDATE hex
    SET tokens = {tokens}
    WHERE id = {tile_id}
    '''

    async with request.app['pool'].acquire() as db_conn:
        cursor = await db_conn.cursor(aiomysql.DictCursor)
        await cursor.execute(query)
        result = cursor.rowcount
        if result == -1:
            message = {
                    'Error': f'Tile with id {tile_id} not found'
                    }
            return web.json_response(message, status=404)
        await db_conn.commit()
        message = {
                'Result': f'Updated tile-id {tile_id}'
                }
        return web.json_response(message, status=200)


async def create_tile(request):
    data = await request.json()
    owner = data.get('owner')
    tokens = data.get('tokens')
    x = data.get('x')
    y = data.get('y')
    playable = data.get('playable')
    board_id = data.get('board_id')
    query = '''
        INSERT INTO hex (owner, tokens, x, y, playable, boardid)
        VALUES (%s, %s, %s, %s, %s, %s)
    '''
    async with request.app['pool'].acquire() as db_conn:
        cursor = await db_conn.cursor(aiomysql.DictCursor)
        await cursor.execute(
                query,
                (
                    owner,
                    tokens,
                    x,
                    y,
                    playable,
                    board_id
                )
            )
        await db_conn.commit()
        db_conn.close()
    return web.json_response(text="hello", status=200)
