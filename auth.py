from typing import Optional

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

API_TOKEN = "kz-cr-api-demo-token"

api_token_header = APIKeyHeader(name="X-API-Token", auto_error=False)


def require_api_token(token: Optional[str] = Security(api_token_header)) -> None:
    """Reject the request unless it carries the valid X-API-Token header."""
    if token is None or token != API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API token",
        )
