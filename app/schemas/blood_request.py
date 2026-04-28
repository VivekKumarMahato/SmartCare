from pydantic import BaseModel,field_validator
from datetime import date
from app.models.enums import BloodGroup
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.donor import Donor
from app.models.blood_request import BloodRequest
from app.models.enums import RequestStatus

class BloodRequestCreate(BaseModel):
    blood_group: BloodGroup
    location: str
    required_date: date

    @field_validator("blood_group", mode="before")
    def normalize_blood_group(cls, value):
        if isinstance(value, str):
            value = value.strip().upper()
        return value


