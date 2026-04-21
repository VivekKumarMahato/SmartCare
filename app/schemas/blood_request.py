from pydantic import BaseModel
from datetime import date

class BloodRequestCreate(BaseModel):
    blood_group: str
    location: str
    required_date: date