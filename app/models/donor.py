from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy import Enum as SqlEnum

from app.db.session import Base
from app.models.enums import BloodGroup


class Donor(Base):
    __tablename__ = "donors"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    blood_group = Column(
        SqlEnum(
            BloodGroup,
            values_callable=lambda obj: [e.value for e in obj]
        ),
        nullable=False
    )

    location = Column(String, nullable=False, index=True)



    is_available = Column(Boolean, default=True, index=True)

    user = relationship("User", back_populates="donor")

    __table_args__ = (
        UniqueConstraint('user_id', name='unique_user_donor'),
    )