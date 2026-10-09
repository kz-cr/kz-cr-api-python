from fastapi import Depends, FastAPI

from auth import require_api_token
from items import router as items_router

app = FastAPI(title="Shopping API", dependencies=[Depends(require_api_token)])

app.include_router(items_router)
