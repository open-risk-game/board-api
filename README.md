# Board API

## Overview

### GET

#### State of a baord

`curl http://<host>/v0/get-board?id=1`

Used when you wish to retrive the state of any given board.

**Response**

``` json
{
    "boardInfo": {
        "id": 1,
        "description": "Test board",
        "created": "2020-07-07 17:17:39",
        "playing": 786,
        "status": "playing",
    },
    "players": [
        {
            "id": 54,
            "colour": "#64232",
            "wins": 0,
            "draws": 0,
            "loses": 0
        },
        {
            "id": 786,
            "colour": "#236982",
            "wins": 0,
            "draws": 0,
            "loses": 0
        }
    ],
    "tiles": [
        {
            "id": 111,
            "owner": 1,
            "tokens": 5,
            "x": 0, 
            "y": 0,
            "playable": 1,
            "neighbors": [112, 113],
        },
        {
            "id": 112,
            "owner": 2,
            "tokens": 7,
            "x": 0,
            "y": 1,
            "playable": 1,
            "neighbors": [111, 113],
        },
        {
            "id": 113,
            "owner": null,
            "tokens": 0,
            "x": 1,
            "y": 0,
            "playable": 0,
            "neighbors": [112, 111],
        }
    ]
}
```

#### State of single tile

`curl http://<host>/v0/get-tile?id=2`

**Response**

```json
{
"id": 111,
"owner": 1,
"tokens": 5,
"x": 0,
"y": 0,
"playable": 1,
"neighbors": [112, 113],
},
```


#### Check connection for between two tiles

`curl http://<host>/v0/check-connection?from=2&to=3`

**Response**

```json
{"Connection": "true"}
```

#### Get which player is next to move

`curl http://<host>/v0/get-turn?id=1`

**Response**

`{"playing": 1}`

### PATCH

#### Update board with next players turn

`curl -X PATCH http://<host>v0/update-turn -d '{"id": 2, "next": 2}'`

**Reponse**

`{"next-player": 2}`

## Development

Test against your local `MySQL` instance. See the `game-database` repository
for latest database schema and test data. The username and password needed for
you database is in the `Makefile`. Don't forget to give your database user full
privileges or you may have trouble running the tests.

## Docker

> docker build -t board-api .

You only need to build this image if you are working on the `game-service`
repository.
