from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auth import require_api_token
from items import router as items_router

# DEMO: intentionally vulnerable - debug mode returns tracebacks to clients (CWE-489)
app = FastAPI(
    title="Shopping API",
    debug=True,
    dependencies=[Depends(require_api_token)],
)

# DEMO: intentionally vulnerable - wildcard origins with credentials (CWE-942)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(items_router)
