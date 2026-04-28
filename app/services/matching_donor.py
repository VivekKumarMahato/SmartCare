from app.core.blood_compatibility import COMPATIBILITY_MAP
from app.models.donor import Donor
from sqlalchemy.orm import Session

def get_matching_donors(db: Session, blood_request):
    compatible_donors = [
        donor_group
        for donor_group, recipients in COMPATIBILITY_MAP.items()
        if blood_request.blood_group in recipients
    ]

    donors = db.query(Donor).filter(
        Donor.blood_group.in_(compatible_donors),
        Donor.location == blood_request.location,
        Donor.is_available == True
    ).all()

    return donors