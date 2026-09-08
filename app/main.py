from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.auth import router as auth_router
from app.api.v1.content import router as content_router
from app.api.v1.media import router as media_router
from app.api.v1.contact import router as contact_router
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs"
)

cors_origins = [
    origin.strip().rstrip("/")
    for origin in settings.CORS_ALLOWED_ORIGINS.split(",")
    if origin.strip()
]

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1/admin/auth", tags=["auth"])
app.include_router(content_router, prefix="/api/v1", tags=["content"])
app.include_router(media_router, prefix="/api/v1", tags=["media"])
app.include_router(contact_router, prefix="/api/v1", tags=["contact"])

@app.get("/api/v1/health")
def health_check():
    return {"status": "ok"}
