from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.blood_request import BloodRequest
from app.models.donor import Donor
from app.models.enums import RequestStatus
from app.core.blood_compatibility import get_compatible_recipients


# ---------------- CREATE REQUEST ----------------
def create_blood_request(db: Session, user_id: int, request):
    new_request = BloodRequest(
        user_id=user_id,
        blood_group=request.blood_group,
        location=request.location,
        required_date=request.required_date,
        status=RequestStatus.pending
    )

    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    return new_request


# ---------------- DONOR VIEW REQUESTS ----------------
def get_donor_available_requests(db: Session, current_user: dict):

    donor = db.query(Donor).filter(
        Donor.user_id == current_user["user_id"]
    ).first()

    if not donor:
        raise HTTPException(status_code=404, detail="Donor profile not found")

    # ---------------- ACTIVE REQUEST CHECK ----------------
    active_request = db.query(BloodRequest).filter(
        BloodRequest.assigned_donor_id == donor.id,
        BloodRequest.status == RequestStatus.accepted
    ).first()

    if active_request:
        raise HTTPException(
            status_code=400,
            detail="You already have an active request"
        )

    if not donor.is_available:
        raise HTTPException(status_code=400, detail="Donor is not available")


    compatible_requests = get_compatible_recipients(donor.blood_group)

    if not compatible_requests:
        raise HTTPException(
            status_code=400,
            detail="Invalid blood group or no compatible recipients found"
        )
    

    # ---------------- FETCH REQUESTS ----------------
    requests = db.query(BloodRequest).filter(
        BloodRequest.blood_group.in_(compatible_requests),
        BloodRequest.location == donor.location,
        BloodRequest.status == RequestStatus.pending
    ).order_by(BloodRequest.required_date).limit(20).all()

    return donor, requests