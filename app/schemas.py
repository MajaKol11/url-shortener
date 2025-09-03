from pydantic import BaseModel, Field

class ShortenRequest(BaseModel):
    #The original URL to be shortened
    url: str = Field(..., max_length=2048, description="The original URL to be shortened")

class ShortenResponse(BaseModel):
    code: str
    short_url: str
    original_url: str