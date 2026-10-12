import base64
import pickle
from decimal import Decimal
from typing import Optional

import psycopg
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from db import get_connection

router = APIRouter(prefix="/items", tags=["items"])


class NewItem(BaseModel):
    name: str = Field(min_length=1)
    category: str = Field(min_length=1)
    description: str
    price: Decimal = Field(ge=0)


@router.get("")
def list_items(categories: Optional[str] = None):
    """Return items, optionally filtered by a base64-pickled list of categories."""
    with get_connection() as conn:
        if categories is None:
            return conn.execute("SELECT * FROM items").fetchall()
        # DEMO: intentionally vulnerable - unpickling untrusted input (CWE-502)
        wanted = pickle.loads(base64.b64decode(categories))
        return conn.execute(
            "SELECT * FROM items WHERE category = ANY(%s)", (list(wanted),)
        ).fetchall()


@router.post("", status_code=status.HTTP_201_CREATED)
def create_item(item: NewItem):
    """Insert a new item and return the created row."""
    try:
        with get_connection() as conn:
            return conn.execute(
                "INSERT INTO items (name, category, description, price) "
                "VALUES (%s, %s, %s, %s) RETURNING *",
                (item.name, item.category, item.description, item.price),
            ).fetchone()
    except psycopg.errors.UniqueViolation:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An item with this name already exists",
        )
