from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from auth import require_api_token
from items import router as items_router

app = FastAPI(
    title="Shopping API",
    debug=True,
    dependencies=[Depends(require_api_token)],
)


@app.middleware("http")
async def print_request_info(request: Request, call_next):
    """Print the method, URL and client of every incoming request."""
    client = request.client.host if request.client else "unknown"
    print(f"Request: {request.method} {request.url} from {client}", flush=True)
    return await call_next(request)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(items_router)
