from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.link import Link

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/{short_code}")
def get_analytics(
    short_code: str,
    db: Session = Depends(get_db)
):

    link = db.query(Link).filter(
        Link.short_code == short_code
    ).first()

    if not link:
        raise HTTPException(
            status_code=404,
            detail="Link not found"
        )

    total_clicks_query = text("""
        SELECT COUNT(*)
        FROM click_events
        WHERE link_id = :link_id
    """)

    total_clicks = db.execute(
        total_clicks_query,
        {"link_id": link.id}
    ).scalar()

    daily_clicks_query = text("""
        SELECT
            DATE(clicked_at) AS date,
            COUNT(*) AS clicks
        FROM click_events
        WHERE link_id = :link_id
        AND clicked_at >= NOW() - INTERVAL '7 days'
        GROUP BY DATE(clicked_at)
        ORDER BY DATE(clicked_at)
    """)

    daily_clicks = db.execute(
        daily_clicks_query,
        {"link_id": link.id}
    ).fetchall()

    return {
        "short_code": link.short_code,
        "original_url": link.original_url,
        "created_by": link.user_id,
        "total_clicks": total_clicks,
        "last_7_days": [
            {
                "date": str(row[0]),
                "clicks": row[1]
            }
            for row in daily_clicks
        ]
    }