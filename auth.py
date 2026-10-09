import secrets

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

API_TOKEN = "kz-cr-api-demo-token"

api_token_header = APIKeyHeader(name="X-API-Token", auto_error=False)


def require_api_token(token: str | None = Security(api_token_header)) -> None:
    """Reject the request unless it carries the valid X-API-Token header."""
    if token is None or not secrets.compare_digest(
        token.encode(), API_TOKEN.encode()
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API token",
        )
