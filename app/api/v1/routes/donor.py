from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.donor import Donor
from app.schemas.donor import DonorCreate
from app.core.security import get_current_user
from sqlalchemy.exc import IntegrityError
from app.services.donor import create_donor_profile
from app.db.dependencies import get_db
router = APIRouter()




@router.post("/create")
def create_donor(
    donor: DonorCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    new_donor = create_donor_profile(db, current_user, donor)

    return {"message": "Donor profile created"}