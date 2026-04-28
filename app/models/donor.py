from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base
from sqlalchemy import Enum as SqlEnum
from app.models.enums import BloodGroup


class Donor(Base):
    __tablename__ = "donors"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)

    blood_group = Column(SqlEnum(BloodGroup), index=True)
    location = Column(String)
    is_available = Column(Boolean, default=True)

    user = relationship("User", back_populates="donor")