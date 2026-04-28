from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.donor import Donor
from app.schemas.donor import DonorCreate
from app.core.security import get_current_user
from sqlalchemy.exc import IntegrityError


def create_donor_profile(db: Session, current_user: dict, donor_data):
    # ---------------- CHECK EXISTING ----------------
    existing = db.query(Donor).filter(
        Donor.user_id == current_user["user_id"]
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Already a donor")

    # ---------------- CREATE ----------------
    new_donor = Donor(
        user_id=current_user["user_id"],
        blood_group=donor_data.blood_group,
        location=donor_data.location
    )

    try:
        db.add(new_donor)
        db.commit()
        db.refresh(new_donor)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Failed to create donor")

    return new_donor