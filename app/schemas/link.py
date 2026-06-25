from pydantic import BaseModel
from datetime import datetime


class CreateLinkRequest(BaseModel):
    url: str
    expiry_date: datetime | None = None