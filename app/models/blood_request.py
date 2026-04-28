from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.db.session import Base
from sqlalchemy import Enum as SqlEnum
from app.models.enums import RequestStatus
from sqlalchemy import Integer, ForeignKey
from sqlalchemy import Enum as SqlEnum
from app.models.enums import BloodGroup

class BloodRequest(Base):
    __tablename__ = "blood_requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    blood_group = Column(
        SqlEnum(
            BloodGroup,
            values_callable=lambda obj: [e.value for e in obj]
        ),
        nullable=False
    )
    location = Column(String)
    required_date = Column(Date)
    status = Column(SqlEnum(RequestStatus), default=RequestStatus.pending)

    user = relationship("User", back_populates="requests")
    assigned_donor_id = Column(Integer, ForeignKey("donors.id"), nullable=True)
    assigned_donor = relationship("Donor")