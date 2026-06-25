from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.link import Link
from app.models.user import User
from app.schemas.link import CreateLinkRequest

from app.utils.dependencies import get_current_user
from app.services.shortener import generate_short_code
from app.services.qr_service import generate_qr_code
from app.config import BASE_URL

router = APIRouter(
    prefix="/links",
    tags=["Links"]
)


@router.post("/")
def create_short_link(
    request: CreateLinkRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Normalize URL
    original_url = request.url.strip()

    if not original_url.startswith(("http://", "https://")):
        original_url = "https://" + original_url

    # Check if this user has already shortened this URL
    existing_link = db.query(Link).filter(
        Link.original_url == original_url,
        Link.user_id == current_user.id
    ).first()

    if existing_link:
        return {
            "message": "URL already shortened",
            "original_url": existing_link.original_url,
            "short_code": existing_link.short_code,
            "short_url": f"{BASE_URL}/r/{existing_link.short_code}",
            "qr_code_url": f"{BASE_URL}/static/qr_codes/{existing_link.short_code}.png"
        }

    # Generate new short code
    short_code = generate_short_code()

    # Safety check to avoid duplicate short codes
    while db.query(Link).filter(
        Link.short_code == short_code
    ).first():
        short_code = generate_short_code()

    # Save new link
    link = Link(
        original_url=original_url,
        short_code=short_code,
        expiry_date=request.expiry_date,
        user_id=current_user.id
    )

    db.add(link)
    db.commit()
    db.refresh(link)

    short_url = f"{BASE_URL}/r/{short_code}"

    generate_qr_code(
        short_url,
        short_code
    )

    return {
        "message": "Short URL created successfully",
        "original_url": original_url,
        "short_code": short_code,
        "short_url": short_url,
        "qr_code_url": f"{BASE_URL}/static/qr_codes/{short_code}.png"
    }