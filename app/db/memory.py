from typing import Dict, Optional, TypedDict
from datetime import datetime, timezone

class UrlRecord(TypedDict):
    original_url: str
    normalized_url: str
    created_at_utc: str
    hit_count: int

#In-memory stores (reset on process restart)
code_to_url: Dict[str, UrlRecord] = {}
url_to_code: Dict[str, str] = {}

def get_code_by_url(noramlized_url: str) -> Optional[str]:
    return url_to_code.get(noramlized_url)

def get_mapping(code: str) -> Optional[UrlRecord]:
    return code_to_url.get(code)

def save_mapping(code: str, original_url: str, normalized_url: str) -> UrlRecord:
    rec: UrlRecord = {
        "original_url": original_url,
        "normalized_url": normalized_url,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "hit_count": 0
    }

    code_to_url[code] = rec
    url_to_code[normalized_url] = code
    return rec

def increment_hit_count(code: str) -> Optional[UrlRecord]:
    """Increase hit_count for a code; return the updated record or None if missing."""
    rec = code_to_url.get(code)
    if rec is None:
        return None
    rec["hit_count"] += 1
    return rec
