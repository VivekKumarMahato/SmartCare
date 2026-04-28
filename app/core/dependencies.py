from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.dependencies import get_db
from app.models.donor import Donor


def require_donor():
    def donor_checker(
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)
    ):
        donor = db.query(Donor).filter(
            Donor.user_id == current_user["user_id"]
        ).first()

        if not donor:
            raise HTTPException(
                status_code=403,
                detail="Donor profile required"
            )

        return current_user

    return donor_checker