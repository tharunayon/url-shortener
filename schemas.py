from pydantic import BaseModel, HttpUrl

class URLBase(BaseModel):
    original_url: HttpUrl

class URLCreate(URLBase):
    pass

class URLResponse(BaseModel):
    original_url: str
    short_url: str
    short_code: str
    clicks: int

    class Config:
        from_attributes = True
