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
  router.py        # GET /items
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
auto-reload on `http://0.0.0.0:8000` (all interfaces, plain HTTP). Override with `HOST` and `PORT`, e.g.
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
wrong token get `401 Unauthorized`. The token is currently hardcoded in `auth.py`
as `kz-cr-api-demo-token` (demo only; move it to an environment variable before
real use).

## Endpoints

### `GET /items`

Returns every row in the `items` table as a JSON array, as-is. There is no
pagination or sorting.

Optional query parameter `categories`: a base64-encoded pickle of a list of category
names (e.g. `["Produce"]`). When present, only items in those categories are returned.

```
curl -H "X-API-Token: kz-cr-api-demo-token" http://localhost:8000/items

# only Produce items
CATS=$(python3 -c 'import base64,pickle;print(base64.b64encode(pickle.dumps(["Produce"])).decode())')
curl -H "X-API-Token: kz-cr-api-demo-token" "http://localhost:8000/items?categories=$CATS"
```

## Known vulnerabilities (intentional demo)

This branch deliberately introduces security flaws so a scanner can detect them.
**Do not deploy or merge to `main`.** Each flaw is marked `# DEMO: intentionally vulnerable`
in the code.

| # | Vulnerability | Location | CWE |
|---|---------------|----------|-----|
| 1 | Plain HTTP, no TLS or HTTPS redirect | `run.sh` | CWE-319 |
| 2 | Binds to all interfaces (`0.0.0.0`) | `run.sh` | CWE-668 |
| 3 | Wildcard CORS with credentials allowed | `main.py` | CWE-942 |
| 4 | Debug mode enabled (tracebacks sent to clients) | `main.py` | CWE-489 |
| 5 | Non-constant-time API token comparison (timing attack) | `auth.py` | CWE-208 |
| 6 | Unsafe deserialization: `pickle.loads` on the `categories` query param (remote code execution) | `items/router.py` | CWE-502 |
| 7 | Hardcoded API token (pre-existing) | `auth.py` | CWE-798 |
