# map-api

## Overview

### GET

#### Game state of a baord

`curl http://<url>/v0/get-board?board_id=1`

Used when you wish to retrive the state of any given board.

`[{"owner": "abc", "tile_id": 1, "tokens": 5}, {"owner": "efg", "tile_id": 2, "tokens": 7}, {"owner": "efg", "tile_id": 3, "tokens": 0}, {"owner": "neutral", "tile_id": 4, "tokens": 0}, {"owner": "neutral", "tile_id": 5, "tokens": 0}]`

## Development

Test against your local `MySQL` instance. See the `game-database` repository
for latest database schema and test data. The username and password needed for
you database is in the `Makefile`. Don't forget to give your database user full
privileges or you may have trouble running the tests.

## Docker

> docker build -t board-api .

You only need to build this image if you are working on the `game-service`
repository.
