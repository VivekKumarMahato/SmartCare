from app.models.donor import Donor

def get_matching_donors(db, blood_request):
    donors = db.query(Donor).filter(
        Donor.blood_group == blood_request.blood_group,
        Donor.location == blood_request.location,
        Donor.is_available == True
    ).all()

    return donors