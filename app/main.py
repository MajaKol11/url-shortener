from datetime import datetime, timezone
from fastapi import FastAPI
from urllib.parse import urlsplit, urlunsplit

app = FastAPI(title="URL Shortener", version="0.1.0")

@app.get("/health", summary="Liveness/health check")
def health():
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.get("/", include_in_schema=False)
def root():
    return {
        "message": "URL Shortener API. See /docs for interactive API."
    }

def _normalize_url(url: str) -> str:
    """
    Minimal normalization:
    - strip whitespace
    - lower-case scheme and host 
    - require http/https and non-empty host
    """
    s = url.strip()
    parts = urlsplit(s)

    scheme = parts.scheme.lower()
    netloc = parts.netlock.lower()

    if scheme not in ("http", "https") or not netloc:
        raise ValueError("Only absolute HTTP/HTTPS URLs are allowed.")
    
    #Rebuild, preserving path/query/fragment as-is
    return urlunsplit((scheme, netloc, parts.path, parts.query, parts.fragment))