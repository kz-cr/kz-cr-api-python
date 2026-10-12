import base64
import pickle
from typing import Optional

from fastapi import APIRouter

from db import get_connection

router = APIRouter(prefix="/items", tags=["items"])


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
