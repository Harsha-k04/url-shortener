from pydantic import BaseModel


class AnalyticsResponse(BaseModel):
    total_clicks: int
    last_7_days: list