from fastapi import FastAPI, Request

from items import router as items_router

app = FastAPI(title="Shopping API")


@app.middleware("http")
async def print_request_info(request: Request, call_next):
    """Print the method, URL and client of every incoming request."""
    client = request.client.host if request.client else "unknown"
    print(f"Request: {request.method} {request.url} from {client}", flush=True)
    return await call_next(request)


app.include_router(items_router)
