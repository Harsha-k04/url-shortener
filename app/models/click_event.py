from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime
)
from sqlalchemy.sql import func

from app.database import Base


class ClickEvent(Base):
    __tablename__ = "click_events"

    id = Column(Integer, primary_key=True)

    link_id = Column(
        Integer,
        ForeignKey("links.id")
    )

    ip_address = Column(String)

    user_agent = Column(String)

    clicked_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )