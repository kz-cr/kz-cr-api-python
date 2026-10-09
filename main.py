from fastapi import FastAPI

from items import router as items_router

app = FastAPI(title="Shopping API")

app.include_router(items_router)
