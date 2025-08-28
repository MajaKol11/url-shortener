from datetime import datetime, timezone
from fastapi import FastAPI

app = FastAPI(title="URL Shortener", version="0.1.0")

@app.get("/health", summary="Liveness/health check")
def health():
    """Return a minimal JSON payload indicating the service is up."""
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.get("/", include_in_schema=False)
def root():
    """Small landing message; hidden from the OpenAPI schema."""
    return {
        "message": "Welcome to the URL Shortener API. See /docs for interactive API."
    }
