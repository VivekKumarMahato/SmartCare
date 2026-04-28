from fastapi import Depends, HTTPException
from app.core.security import get_current_user

def require_role(required_roles: list):
    def role_checker(current_user: dict = Depends(get_current_user)):
        user_role = current_user.get("role")

        if user_role not in required_roles:
            raise HTTPException(
                status_code=403,
                detail="Permission denied"
            )

        return current_user

    return role_checker