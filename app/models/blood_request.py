from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.db.session import Base

class BloodRequest(Base):
    __tablename__ = "blood_requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    blood_group = Column(String, index=True)
    location = Column(String)
    required_date = Column(Date)
    status = Column(String, default="pending")

    user = relationship("User", back_populates="requests")