from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.blood_request import BloodRequest
from app.models.donor import Donor
from app.models.enums import RequestStatus

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


def get_donor_available_requests(db: Session, current_user: dict):
    # ---------------- FETCH DONOR ----------------
    donor = db.query(Donor).filter(
        Donor.user_id == current_user["user_id"]
    ).first()

    if not donor:
        raise HTTPException(status_code=404, detail="Donor profile not found")

    if not donor.is_available:
        raise HTTPException(status_code=400, detail="Donor is not available")

    # ---------------- FETCH REQUESTS ----------------
    requests = db.query(BloodRequest).filter(
        BloodRequest.blood_group == donor.blood_group,
        BloodRequest.location == donor.location,
        BloodRequest.status == RequestStatus.pending
    ).all()

    return donor, requests