# kz-cr-api-python

Python API backend for a shopping web application, built with FastAPI and PostgreSQL.

## Project structure

The root directory holds the entry point; each API capability lives in its own
subfolder and exposes a router that `main.py` includes.

```
main.py            # entry point, includes each capability's router
db.py              # Postgres connection helper
auth.py            # API token check applied to every endpoint
items/
  __init__.py
  router.py        # GET /items, POST /items
requirements.txt
run.sh             # local run script
```

To add a capability, create a new subfolder with a `router` and include it in `main.py`.

## Running locally

Requires Python 3 and a PostgreSQL database reachable on `localhost:5432`.

```
./run.sh
```

This creates `.venv` if missing, installs `requirements.txt`, and starts uvicorn with
auto-reload on `http://0.0.0.0:8000`. Override with `HOST` and `PORT`, e.g.
`PORT=9000 ./run.sh`. Interactive docs are at `/docs`.

## Configuration

Database settings are read from environment variables:

| Variable      | Default        |
|---------------|----------------|
| `DB_HOST`     | `localhost`    |
| `DB_PORT`     | `5432`         |
| `DB_USER`     | `app`          |
| `DB_PASSWORD` | `app_password` |
| `DB_NAME`     | `app`          |

## Authentication

Every endpoint requires an `X-API-Token` request header. Requests with a missing or
wrong token get `401 Unauthorized`. The expected token is defined in `auth.py`.

## Endpoints

### `GET /items`

Returns every row in the `items` table as a JSON array, as-is. There is no
pagination, sorting or filtering yet.

```
curl -H "X-API-Token: kz-cr-api-demo-token" http://localhost:8000/items
```

### `POST /items`

Creates an item from a JSON body and returns the created row (including its generated
`id`) with `201 Created`. `name` and `category` must be non-empty, `description` is
required, and `price` must be `>= 0`. Names are unique: a duplicate returns `409 Conflict`,
and an invalid body returns `422`.

```
curl -X POST http://localhost:8000/items \
  -H "X-API-Token: kz-cr-api-demo-token" \
  -H "Content-Type: application/json" \
  -d '{"name": "Whole Milk", "category": "Dairy", "description": "1 gallon whole milk.", "price": 3.49}'
```
