from fastapi import APIRouter

from db import get_connection

router = APIRouter(prefix="/items", tags=["items"])


@router.get("")
def list_items():
    """Return all rows from the items table as-is."""
    with get_connection() as conn:
        return conn.execute("SELECT * FROM items").fetchall()
