from pydantic import BaseModel
from app.models.enums import BloodGroup
class DonorCreate(BaseModel):
    blood_group: BloodGroup
    location: str