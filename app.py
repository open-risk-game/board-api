import os
import aiomysql
import logging
from aiohttp import web
import models.board as board
import models.hexagon as hexagon


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
        web.get('/v0/check-connection', hexagon.is_connected),
        web.get('/v0/get-hex', hexagon.get_hex),
        web.get('/v0/get-board', board.get_board),
        web.patch('/v0/change-ownership', hexagon.change_ownership),
        web.patch('/v0/update-tokens', hexagon.update_tokens),
        ])

logging.basicConfig(
        filename="board.log",
        format='%(asctime)s - %(message)s',
        level=logging.INFO
        )

if __name__ == "__main__":
    web.run_app(app)
