from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine

# Import models so SQLAlchemy creates the tables
from app.models.user import User
from app.models.link import Link
from app.models.click_event import ClickEvent

# Import routers
from app.routers.auth import router as auth_router
from app.routers.links import router as links_router
from app.routers.analytics import router as analytics_router
from app.routers.redirect import router as redirect_router
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded

from app.limiter import limiter

# Create database tables
Base.metadata.create_all(bind=engine)

# Base directory
BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="URL Shortener API",
    description="A URL Shortener with JWT Authentication, Analytics and QR Code Generation",
    version="1.0.0"
)
app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)

# Serve static files
app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)

# Register routers
app.include_router(auth_router)
app.include_router(links_router)
app.include_router(analytics_router)

# Root endpoint
@app.get("/")
def home():
    return {
        "message": "Database Connected Successfully"
    }


@app.exception_handler(RateLimitExceeded)
async def custom_rate_limit_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={
            "detail": "Too many requests. Please try again after one minute."
        }
    )
    
@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
    
app.include_router(redirect_router)