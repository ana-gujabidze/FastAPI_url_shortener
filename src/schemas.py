# src/schemas.py

from typing import Optional

from pydantic import BaseModel, constr


class URLBase(BaseModel):
    target_url: str
    custom_code: Optional[constr(max_length=9)] = None


class URL(URLBase):
    clicks: int

    class Config:
        orm_mode = True


class URLInfo(URL):
    url: str
    admin_url: str
