from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.donor import Donor
from app.schemas.donor import DonorCreate
from app.core.security import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/create")
def create_donor(
    donor: DonorCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    new_donor = Donor(
        user_id=current_user["user_id"],
        blood_group=donor.blood_group,
        location=donor.location
    )

    db.add(new_donor)
    db.commit()

    return {"message": "Donor profile created"}