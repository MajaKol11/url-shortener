from pydantic import BaseModel, Field

class ShortenRequest(BaseModel):
    #The original URL to be shortened
    url: str = Field(..., max_length=2048, description="The original URL to be shortened")

class ShortenResponse(BaseModel):
    code: str
    short_url: str      #relaxed to str to avoid localhost validation issues
    original_url: str

class StatsResponse(BaseModel):
    code: str
    original_url: str
    created_at_utc: str
    hit_count: int