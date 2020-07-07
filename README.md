# Board API

## Overview

### GET

#### State of a baord

`curl http://<host>/v0/get-board?id=1`

Used when you wish to retrive the state of any given board.

**Response**

``` json
{
    "board-info": {
        "id": 1,
        "description": "Test board",
        "created": "2020-07-07 17:17:39",
        "playerAid": 1,
        "playerBid": 2,
    }
    "hexagons": [
        {
            "hex_id": 111,
            "player_id": 1,
            "tokens": 5,
            "x": 0, 
            "y": 0,
            "playable": 1,
            "neighbors": [112, 113],
        },
        {
            "hex_id": 112,
            "player_id": 2,
            "tokens": 7,
            "x": 0,
            "y": 1,
            "playable": 1,
            "neighbors": [111, 113],
        },
        {
            "hex_id": 113,
            "player_id": null,
            "tokens": 0,
            "x": 1,
            "y": 0,
            "playable": 0,
            "neighbors": [112, 111],
        }
    ]
}
```

#### State of single hexagon

`curl http://<host>/v0/get-hex?id=2`

**Response**

```json
{
"hex_id": 111,
"player_id": 1,
"tokens": 5,
"x": 0,
"y": 0,
"playable": 1,
"neighbors": [112, 113],
},
```


#### Check connection for between two hexagons

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
