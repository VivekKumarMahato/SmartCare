from pydantic import BaseModel, EmailStr, Field, field_validator


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    phone: str = Field(min_length=10, max_length=15)
    address: str = Field(min_length=5, max_length=200)
    password: str = Field(min_length=6, max_length=100)



    @field_validator("password")
    def validate_password(cls, value):
        if value.isdigit():
            raise ValueError("Password cannot be only numbers")
        return value

    @field_validator("phone")
    def validate_phone(cls, value):
        if not value.isdigit():
            raise ValueError("Phone must contain only digits")
        return value

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)