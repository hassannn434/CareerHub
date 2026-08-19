from fastapi import APIRouter, Depends
from ..db.session import get_db
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/health", tags=["health"])
def health_check(db: Session = Depends(get_db)):
    # simple DB query to validate connection
    try:
        # lightweight check
        db.execute("SELECT 1")
        return {"status": "ok", "db": "connected"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
