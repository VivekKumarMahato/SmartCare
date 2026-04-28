from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.models.blood_request import BloodRequest
from app.models.donor import Donor
from app.models.enums import RequestStatus
from app.schemas.blood_request import BloodRequestCreate
from app.core.security import get_current_user
from app.core.dependencies import require_donor
from app.services.blood_request import (create_blood_request,
    get_donor_available_requests
)
from app.services.matching_donor import get_matching_donors
from app.services.update_request_status import update_request_status

router = APIRouter()


# ---------------- CREATE REQUEST ----------------
@router.post("/create")
def create_request(
    request: BloodRequestCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    new_request = create_blood_request(
        db=db,
        user_id=current_user["user_id"],
        request=request
    )

    return {
        "id": new_request.id,
        "message": "Blood request created"
    }


# ---------------- MATCH DONORS ----------------
@router.get("/match/{request_id}")
def match_donors(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    blood_request = db.query(BloodRequest).filter(
        BloodRequest.id == request_id
    ).first()

    if not blood_request:
        raise HTTPException(status_code=404, detail="Request not found")

    # ---------------- CASE 1: PENDING ----------------
    if blood_request.status == RequestStatus.pending:
        donors = get_matching_donors(db, blood_request)

        return {
            "request_id": blood_request.id,
            "status": blood_request.status.value,
            "matching_donors": [
                {
                    "id": donor.id,
                    "blood_group": donor.blood_group,
                    "location": donor.location
                }
                for donor in donors
            ]
        }

    # ---------------- CASE 2: ACCEPTED ----------------
    elif blood_request.status == RequestStatus.accepted:

        if not blood_request.assigned_donor_id:
            raise HTTPException(status_code=400, detail="No donor assigned")

        donor = db.query(Donor).filter(
            Donor.id == blood_request.assigned_donor_id
        ).first()

        if not donor:
            raise HTTPException(status_code=404, detail="Assigned donor not found")

        return {
            "request_id": blood_request.id,
            "status": blood_request.status.value,
            "assigned_donor": {
                "name": donor.user.name,
                "phone": donor.user.phone,
                "location": donor.location
            }
        }

    # ---------------- CASE 3: COMPLETED ----------------
    else:
        return {
            "request_id": blood_request.id,
            "status": blood_request.status.value,
            "message": "Request already completed"
        }

# ---------------- GET MY REQUESTS ----------------
@router.get("/my")
def get_my_requests(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    requests = db.query(BloodRequest).filter(
        BloodRequest.user_id == current_user["user_id"]
    ).all()

    return {
        "total": len(requests),
        "requests": [
            {
                "id": req.id,
                "blood_group": req.blood_group,
                "location": req.location,
                "status": req.status.value,
                "assigned_donor_id": req.assigned_donor_id
            }
            for req in requests
        ]
    }


# ---------------- DONOR REQUESTS ----------------
@router.get("/donor")
def get_donor_requests(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    donor, requests = get_donor_available_requests(db, current_user)

    return {
        "donor_id": donor.id,
        "available_requests": [
            {
                "id": req.id,
                "blood_group": req.blood_group,
                "location": req.location,
                "status": req.status.value
            }
            for req in requests
        ]
    }


# ---------------- UPDATE STATUS ----------------
@router.put("/update-status/{request_id}")
def update_status(
    request_id: int,
    status: RequestStatus,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    updated = update_request_status(db, request_id, status, current_user)

    return updated


# ---------------- ADMIN PENDING----------------
# @router.get("/admin")
# def get_all_requests(
#     db: Session = Depends(get_db),
#     current_user: dict = Depends(require_role(["admin"]))
# ):
#     requests = db.query(BloodRequest).all()
#
#     return {
#         "total": len(requests),
#         "requests": [
#             {
#                 "id": req.id,
#                 "blood_group": req.blood_group,
#                 "location": req.location,
#                 "status": req.status.value,
#                 "assigned_donor_id": req.assigned_donor_id
#             }
#             for req in requests
#         ]
#     }