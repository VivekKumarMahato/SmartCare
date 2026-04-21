from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.blood_request import BloodRequest
from app.schemas.blood_request import BloodRequestCreate
from app.core.security import get_current_user
from app.models.donor import Donor
from app.core.security import get_current_user
from fastapi import HTTPException

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/create")
def create_request(
    request: BloodRequestCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    new_request = BloodRequest(
        user_id=current_user["user_id"],
        blood_group=request.blood_group,
        location=request.location,
        required_date=request.required_date
    )

    db.add(new_request)
    db.commit()

    return {"message": "Blood request created"}


from app.models.donor import Donor


@router.get("/match/{request_id}")
def match_donors(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # Get the request
    blood_request = db.query(BloodRequest).filter(BloodRequest.id == request_id).first()

    if not blood_request:
        return {"error": "Request not found"}

    # Find matching donors
    donors = db.query(Donor).filter(
        Donor.blood_group == blood_request.blood_group,
        Donor.location == blood_request.location,
        Donor.is_available == True
    ).all()

    return {
        "request": blood_request.id,
        "matching_donors": [
            {
                "id": donor.id,
                "location": donor.location,
                "blood_group": donor.blood_group
            }
            for donor in donors
        ]
    }


@router.put("/update-status/{request_id}")
def update_status(
    request_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    blood_request = db.query(BloodRequest).filter(BloodRequest.id == request_id).first()

    if not blood_request:
        raise HTTPException(status_code=404, detail="Request not found")

    # Optional: only owner can update
    if blood_request.user_id != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="Not allowed")

    blood_request.status = status
    db.commit()

    if status == "completed":
        donor = db.query(Donor).filter(
            Donor.blood_group == blood_request.blood_group,
            Donor.location == blood_request.location
        ).first()

        if donor:
            donor.is_available = False

    db.commit()

    return {"message": f"Request {status}"}