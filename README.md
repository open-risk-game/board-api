# map-api

## Overview

### GET

#### Game state of a baord

`curl http://<url>/v0/get-board?board_id=1`

Used when you wish to retrive the state of any given board.

**Response**

``` json
[
    {
    "player_id": 1,
    "tokens": 5,
    "x": 4, "y": 1},
    "neighbors: [2, 3],
    playable: 1,
    },
    {
    "player_id": 2,
    "tokens": 7,
    "x": 0,
    "y": 1
    "neighbors: [1, 3],
    playable: 1,
    },
    {
    "player_id": null,
    "tokens": 0,
    "x": null,
    "y": null},
    "neighbors: [2, 1],
    playable: 0,
    }
]
```

## Development

Test against your local `MySQL` instance. See the `game-database` repository
for latest database schema and test data. The username and password needed for
you database is in the `Makefile`. Don't forget to give your database user full
privileges or you may have trouble running the tests.

## Docker

> docker build -t board-api .

You only need to build this image if you are working on the `game-service`
repository.
