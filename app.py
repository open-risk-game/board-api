import os
import aiomysql
import logging
from aiohttp import web
from models.territory import Territory
from models.region import Region

DB_HOST = os.environ.get('DB_HOST')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_NAME = os.environ.get('DB_NAME')
DB_PORT = int(os.environ.get('DB_PORT'))


async def create_db_pool(app):
    app['pool'] = await aiomysql.create_pool(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            db=DB_NAME,
            port=DB_PORT
        )

app = web.Application()

app.on_startup.append(create_db_pool)

app.add_routes([
        web.get('/v0/get-region', Region.get),
        web.get('/v0/get-territory', Territory.get),
        web.get('/v0/get-boarders', Territory.get_boarders),
        web.get('/v0/get-by-player', Territory.get_by_player),
        web.patch('/v0/add-tokens', Territory.add_tokens),
        web.patch('/v0/change-ownership', Territory.change_ownership),
        ])

logging.basicConfig(
        filename="board.log",
        format='%(asctime)s - %(message)s',
        level=logging.INFO
        )

if __name__ == "__main__":
    web.run_app(app)
