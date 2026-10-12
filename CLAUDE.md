# CLAUDE.md

Python API backend for a shopping web application, built with FastAPI and PostgreSQL (psycopg 3).
See `README.md` for run instructions and the endpoint reference.

## Project structure

```
main.py            # entry point: creates the FastAPI app, includes each capability's router
db.py              # Postgres connection helper (get_connection)
auth.py            # require_api_token dependency (X-API-Token header), applied app-wide in main.py
items/
  __init__.py      # re-exports `router`
  router.py        # GET /items, POST /items
requirements.txt   # fastapi, uvicorn[standard], psycopg[binary]
run.sh             # creates .venv, installs deps, starts uvicorn with --reload
```

## Design patterns and conventions

- **One folder per capability (feature package).** Each API capability lives in its own subfolder and exposes a single `router` (an `APIRouter`) via its `__init__.py` (`from .router import router` + `__all__ = ["router"]`). `main.py` imports it as `from <pkg> import router as <pkg>_router` and calls `app.include_router(...)`. To add a capability, create the folder and register it in `main.py`.
- **Router conventions.** `APIRouter(prefix="/<resource>", tags=["<resource>"])`. The list route uses the empty path `""` (so `GET /items`, not `/items/`). Route handlers carry a one-line docstring.
- **Plain SQL, no ORM.** Queries are raw SQL strings executed through psycopg. Always use parameterized queries (`conn.execute("... WHERE id = %s", (id,))`) — never interpolate user input into SQL.
- **Connection per request via context manager.** `db.get_connection()` opens a new connection with `row_factory=dict_row`, so rows come back as dicts that FastAPI serializes straight to JSON. Use it as `with get_connection() as conn:` in handlers; there is no connection pool or global connection yet.
- **Sync handlers.** Handlers are plain `def` (not `async def`) because psycopg is used synchronously; FastAPI runs them in a threadpool. Do not call blocking DB code from an `async def` handler.
- **Configuration via environment variables.** DB settings (`DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`) are read in `db.py` with local-dev defaults. Do not hardcode other secrets; `.env` is git-ignored.
- **Request logging.** `main.py` has an HTTP middleware that `print`s each request's method, URL and client. Do not print headers or bodies (they can contain credentials).
- **Minimal responses.** Endpoints currently return DB rows as-is, with no Pydantic response models, pagination or sorting (`GET /items` has an optional `category` filter). Request bodies use Pydantic models (e.g. `NewItem`). Add these deliberately when needed and document them in `README.md`.

## Code style

- Imports: stdlib, third-party, then local, separated by blank lines.
- Keep modules small and focused; short docstrings, few comments.
- Dependencies are unpinned in `requirements.txt`; add new ones there.

## Running and checking

- Run locally with `./run.sh` (serves on `http://127.0.0.1:8000`, docs at `/docs`; override with `HOST`/`PORT`). Requires PostgreSQL on `localhost:5432`.
- There is no test suite or linter configured yet. Verify changes by running the app and exercising the endpoint (e.g. `curl http://localhost:8000/items`).
- Keep `README.md` in sync when adding endpoints, config variables, or changing structure.
