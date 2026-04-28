from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.donor import Donor
from app.schemas.donor import DonorCreate
from app.core.security import get_current_user
from app.services.donor import create_donor_profile
from app.db.dependencies import get_db

router = APIRouter()

# ---------------- CREATE DONOR ----------------
@router.post("/create")
def create_donor(
    donor: DonorCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    new_donor = create_donor_profile(db, current_user, donor)

    return {
        "message": "Donor profile created",
        "donor_id": new_donor.id,
        "blood_group": new_donor.blood_group,
        "location": new_donor.location
    }


# ---------------- GET MY DONOR PROFILE ----------------
@router.get("/me")
def get_my_donor_profile(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    donor = db.query(Donor).filter(
        Donor.user_id == current_user["user_id"]
    ).first()

    if not donor:
        raise HTTPException(status_code=404, detail="Donor profile not found")

    return {
        "id": donor.id,
        "blood_group": donor.blood_group,
        "location": donor.location,
        #"phone": donor.phone,
        "is_available": donor.is_available
    }