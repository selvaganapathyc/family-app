from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.auth import verify_token

http_bearer = HTTPBearer(auto_error=True)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> dict:
    """
    FastAPI dependency that extracts the Bearer token from the Authorization
    header, verifies it, and returns the user dict { user_id, email }.
    """
    token = credentials.credentials
    user = verify_token(token)
    return user
