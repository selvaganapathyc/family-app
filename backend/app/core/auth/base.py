from abc import ABC, abstractmethod


class AuthProvider(ABC):
    @abstractmethod
    def verify_token(self, token: str) -> dict:
        """
        Verify an auth token and return user info.
        Must return: { "user_id": str, "email": str }
        Must raise HTTPException 401 if token is invalid or expired.
        """
