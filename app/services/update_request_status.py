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
    # ---------------- FETCH REQUEST ----------------
    blood_request = db.query(BloodRequest).filter(
        BloodRequest.id == request_id
    ).first()

    if not blood_request:
        raise HTTPException(status_code=404, detail="Request not found")

    current_status = blood_request.status
    user_role = current_user.get("role")

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

    # ---------------- ROLE-BASED CONTROL ----------------
    if status == RequestStatus.accepted and user_role != "donor":
        raise HTTPException(status_code=403, detail="Only donors can accept")

    if status == RequestStatus.completed and user_role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can complete")

    # ---------------- PATIENT OWNERSHIP ----------------
    if user_role == "patient" and blood_request.user_id != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="Not allowed")

    # ---------------- ACCEPT LOGIC ----------------
    if status == RequestStatus.accepted:
        donor = db.query(Donor).filter(
            Donor.user_id == current_user["user_id"]
        ).first()

        if not donor:
            raise HTTPException(status_code=404, detail="Donor profile not found")

        if not donor.is_available:
            raise HTTPException(status_code=400, detail="Donor not available")

        if donor.blood_group != blood_request.blood_group:
            raise HTTPException(status_code=400, detail="Blood group mismatch")

        if donor.location != blood_request.location:
            raise HTTPException(status_code=400, detail="Location mismatch")

        # ⚠️ IMPORTANT: check if already assigned
        if blood_request.assigned_donor_id:
            raise HTTPException(status_code=400, detail="Already accepted")

        blood_request.assigned_donor_id = donor.id

    # ---------------- COMPLETE LOGIC ----------------
    if status == RequestStatus.completed:
        if not blood_request.assigned_donor_id:
            raise HTTPException(status_code=400, detail="No donor assigned")

        donor = db.query(Donor).filter(
            Donor.id == blood_request.assigned_donor_id
        ).first()

        if donor:
            donor.is_available = False

    # ---------------- FINAL UPDATE ----------------
    blood_request.status = status
    db.commit()
    db.refresh(blood_request)

    return blood_request