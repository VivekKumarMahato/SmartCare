from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.donor import Donor


def create_donor_profile(db: Session, current_user: dict, donor_data):
    # ---------------- CHECK EXISTING ----------------
    existing = db.query(Donor).filter(
        Donor.user_id == current_user["user_id"]
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="User is already a donor")

    # ---------------- CREATE ----------------
    new_donor = Donor(
        user_id=current_user["user_id"],
        blood_group=donor_data.blood_group,
        location=donor_data.location,
        #phone=donor_data.phone,
        is_available=True
    )

    try:
        db.add(new_donor)
        db.commit()
        db.refresh(new_donor)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="User already registered as donor"
        )

    return new_donor