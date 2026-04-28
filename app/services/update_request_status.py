from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.blood_request import BloodRequest
from app.models.donor import Donor
from app.models.enums import RequestStatus


def update_request_status(
    db: Session,
    request_id: int,
    status: RequestStatus,
    current_user: dict
):
# ---------------- LOCK REQUEST (prevents race condition) ----------------
    blood_request = db.query(BloodRequest).filter(
        BloodRequest.id == request_id
    ).with_for_update().first()

    if not blood_request:
        raise HTTPException(status_code=404, detail="Request not found")

    current_status = blood_request.status

# ---------------- STATE TRANSITIONS ----------------
    valid_transitions = {
        RequestStatus.pending: [RequestStatus.accepted],
        RequestStatus.accepted: [RequestStatus.completed],
        RequestStatus.completed: []
    }

    if status not in valid_transitions[current_status]:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid transition from {current_status} to {status}"
        )

# ---------------- ACCEPT LOGIC ----------------
    if status == RequestStatus.accepted:


        donor = db.query(Donor).filter(
            Donor.user_id == current_user["user_id"]
        ).first()

        if not donor:
            raise HTTPException(status_code=403, detail="You are not a donor")

# ---------- checking  donor availability -------------
        if not donor.is_available:
            raise HTTPException(status_code=400, detail="You already have an active request")


        active_request = db.query(BloodRequest).filter(
            BloodRequest.assigned_donor_id == donor.id,
            BloodRequest.status == RequestStatus.accepted
        ).first()

        if active_request:
            raise HTTPException(status_code=400, detail="You already have an active request")


        if donor.blood_group != blood_request.blood_group:
            raise HTTPException(status_code=400, detail="Blood group mismatch")

        if donor.location != blood_request.location:
            raise HTTPException(status_code=400, detail="Location mismatch")

        if blood_request.assigned_donor_id:
            raise HTTPException(status_code=400, detail="Request already accepted")


        blood_request.assigned_donor_id = donor.id

    # --------  IMPORTANT: block donor from accepting more-------------------
        donor.is_available = False


        donor_info = {
            "name": donor.user.email,   # replace with name if exists
            "location": donor.location,
            "phone": donor.user.phone
        }

    # ---------------- COMPLETE LOGIC ----------------
    elif status == RequestStatus.completed:

        if not blood_request.assigned_donor_id:
            raise HTTPException(status_code=400, detail="No donor assigned")

        donor = db.query(Donor).filter(
            Donor.id == blood_request.assigned_donor_id
        ).first()

        if donor:
            donor.is_available = True

        donor_info = None

    else:
        donor_info = None

    # ---------------- FINAL UPDATE ----------------
    blood_request.status = status
    db.commit()
    db.refresh(blood_request)

    return {
        "request_id": blood_request.id,
        "status": blood_request.status.value,
        "assigned_donor_id": blood_request.assigned_donor_id,
        "donor_info": donor_info
    }