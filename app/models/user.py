from sqlalchemy import Column, Integer, String
from app.db.session import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Enum as SqlEnum
from app.models.enums import UserRole

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(SqlEnum(UserRole), default=UserRole.patient)
    donor = relationship("Donor", back_populates="user", uselist=False)

    requests = relationship("BloodRequest", back_populates="user")