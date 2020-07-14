import os
import aiomysql
import logging
import aiohttp_cors
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
        web.get('/v0/get-turn', board.get_turn),
        web.patch('/v0/change-ownership', hexagon.change_ownership),
        web.patch('/v0/update-tokens', hexagon.update_tokens),
        web.patch('/v0/update-turn', board.update_turn),
        web.post('/v0/create-board', board.create_board),
        web.post('/v0/create-hex', hexagon.create_hex),
        ])

cors = aiohttp_cors.setup(app)
resource = cors.add(app.router.add_resource("/v0/get-board"))
route = cors.add(
    resource.add_route("GET", board.get_board), {
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers=("X-Custom-Server-Header",),
            allow_headers=("X-Requested-With", "Content-Type"),
            max_age=3600,
        )
    })

logging.basicConfig(
        filename="board.log",
        format='%(asctime)s - %(message)s',
        level=logging.INFO
        )

if __name__ == "__main__":
    web.run_app(app)
