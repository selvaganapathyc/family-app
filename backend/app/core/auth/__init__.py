"""
Auth abstraction layer.
Reads AUTH_PROVIDER from config and loads the matching provider.
All other code imports verify_token from here — never from a provider directly.

To switch providers: change AUTH_PROVIDER in your .env file.
Supported values: "supabase" (default)
"""
from app.core.config import settings

_PROVIDERS = {
    "supabase": "app.core.auth.providers.supabase.SupabaseAuthProvider",
    # "clerk":  "app.core.auth.providers.clerk.ClerkAuthProvider",
    # "custom": "app.core.auth.providers.custom_jwt.CustomJWTAuthProvider",
}

def _load_provider():
    provider_name = getattr(settings, "AUTH_PROVIDER", "supabase")
    class_path = _PROVIDERS.get(provider_name)
    if not class_path:
        raise ValueError(f'Unknown auth provider: "{provider_name}". Check AUTH_PROVIDER in your .env file.')
    module_path, class_name = class_path.rsplit(".", 1)
    import importlib
    module = importlib.import_module(module_path)
    return getattr(module, class_name)()

_provider = _load_provider()


def verify_token(token: str) -> dict:
    return _provider.verify_token(token)
