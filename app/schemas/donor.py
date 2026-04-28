from pydantic import BaseModel, Field, field_validator
from app.models.enums import BloodGroup


class DonorCreate(BaseModel):
    blood_group: BloodGroup
    location: str = Field(min_length=2, max_length=100)
    #phone: str = Field(min_length=10, max_length=15)

    # @field_validator("phone")
    # def validate_phone(cls, value):
    #     if not value.isdigit():
    #         raise ValueError("Phone must contain only digits")
    #     return value

    @field_validator("blood_group", mode="before")
    def normalize_blood_group(cls, value):
        if isinstance(value, str):
            value = value.strip().upper()
        return value