from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.modules.finance.router import router as finance_router
from app.modules.health.router import router as health_router
from app.modules.overview.router import router as overview_router

app = FastAPI(
    title="Family App API",
    description="Backend API for the Family personal management app",
    version="1.0.0",
)

# ─── CORS ─────────────────────────────────────────────────────────────────────
# In development, allow all origins.
# For production, restrict to the Railway frontend URL via environment variable.
if settings.ENVIRONMENT == "dev":
    allow_origins = ["*"]
else:
    allow_origins = [
        "https://your-railway-frontend-url",  # Replace after deployment
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Routers ──────────────────────────────────────────────────────────────────
app.include_router(overview_router, prefix="/overview")
app.include_router(finance_router)
app.include_router(health_router, prefix="/health")


# ─── Health check ─────────────────────────────────────────────────────────────
@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "environment": settings.ENVIRONMENT}
