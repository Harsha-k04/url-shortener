from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import SessionLocal
from app.models.link import Link
from app.models.click_event import ClickEvent
from app.limiter import limiter

router = APIRouter(
    prefix="/r",
    tags=["Redirect"]
)


@router.get("/{short_code}")
@limiter.limit("10/minute")
def redirect_url(
    short_code: str,
    request: Request
):

    db: Session = SessionLocal()

    try:

        link = db.query(Link).filter(
            Link.short_code == short_code
        ).first()

        if not link:
            raise HTTPException(
                status_code=404,
                detail="Short URL not found"
            )

        if (
            link.expiry_date
            and datetime.utcnow() > link.expiry_date
        ):
            raise HTTPException(
                status_code=410,
                detail="Link expired"
            )

        click = ClickEvent(
            link_id=link.id,
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent")
        )

        db.add(click)
        db.commit()

        return RedirectResponse(
            url=link.original_url
        )

    finally:
        db.close()