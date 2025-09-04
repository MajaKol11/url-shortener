from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.responses import RedirectResponse, FileResponse
from urllib.parse import urlsplit, urlunsplit, urljoin
from .schemas import ShortenRequest, StatsResponse
from .utils.codes import generate_code, RESERVED
from .db import memory
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="URL Shortener", version="0.1.0")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/health", summary="Liveness/health check")
def health():
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.get("/", include_in_schema=False)
def landing_page():
    return FileResponse("static/index.html")

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
    netloc = parts.netloc.lower()

    if scheme not in ("http", "https") or not netloc:
        raise ValueError("Only absolute HTTP/HTTPS URLs are allowed.")
    
    #Rebuild, preserving path/query/fragment as-is
    return urlunsplit((scheme, netloc, parts.path, parts.query, parts.fragment))


@app.post(
    "/api/shorten",
    status_code=status.HTTP_201_CREATED,
    summary="Create a shortened URL",
)
def create_short_url(payload: ShortenRequest, request: Request, response: Response):
    original_url = str(payload.url)

    if len(original_url) > 2048:
        raise HTTPException(status_code=400, detail="URL is too long (max 2048 characters).")
    
    try:
        normalized = _normalize_url(original_url)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    existing_code = memory.get_code_by_url(normalized)
    if existing_code:
        code = existing_code
    else:
        #Generate unique, non-reserved code
        while True:
            code = generate_code(8)
            if code in RESERVED:
                continue
            if memory.get_mapping(code) is None:
                break
        memory.save_mapping(code, original_url=original_url, normalized_url=normalized)

    short_url = urljoin(str(request.base_url), code)

    response.headers["Location"] = short_url
    return {"short_url": short_url, "code": code, "original_url": original_url}


@app.get(
    "/{code}",
    include_in_schema=False,
    summary="Follow a shortened code"
)
def follow_short_code(code: str):
    """
    Look up the short code, increment its hit counter, and redirect to the original URL. 
    Returns 404 if the code doesn't exist.
    """
    rec=memory.get_mapping(code)
    if rec is None: 
        raise HTTPException(status_code=404, detail="Short code not found.")
    
    memory.increment_hit_count(code)
    return RedirectResponse(url=rec["original_url"], status_code=status.HTTP_307_TEMPORARY_REDIRECT)

@app.get(
    "/api/stats/{code}",
    response_model=StatsResponse,
    summary="Get stats for a short code"
)
def get_stats(code: str):
    """
    Return metadata for a short code:
    - original_url
    - created_at_utc
    - hit_count
    404 if the code doesn't exist
    """
    rec = memory.get_mapping(code)
    if rec is None:
        raise HTTPException(status_code=404, detail="Short code not found.")

    return StatsResponse(
        code=code,
        original_url=rec["original_url"],
        created_at_utc=rec["created_at_utc"],
        hit_count=rec["hit_count"]
    )


