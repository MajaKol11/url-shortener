from pydantic import BaseModel, AnyHttpUrl, Field

class ShortenRequest(BaseModel):
    #The original URL to be shortened
    url: AnyHttpUrl = Field(..., max_length=2048, description="The original URL to be shortened")

class ShortenResponse(BaseModel):
    code: str
    short_url: AnyHttpUrl
    original_url: AnyHttpUrl