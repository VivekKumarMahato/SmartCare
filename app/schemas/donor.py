from pydantic import BaseModel

class DonorCreate(BaseModel):
    blood_group: str
    location: str