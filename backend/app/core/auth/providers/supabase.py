from fastapi import HTTPException, status
from app.core.auth.base import AuthProvider
from app.core.database import get_supabase_client


class SupabaseAuthProvider(AuthProvider):
    def verify_token(self, token: str) -> dict:
        try:
            supabase = get_supabase_client()
            response = supabase.auth.get_user(token)
            user = response.user
            if not user:
                raise self._unauthorized()
            return {"user_id": user.id, "email": user.email}
        except HTTPException:
            raise
        except Exception:
            raise self._unauthorized()

    def _unauthorized(self):
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
