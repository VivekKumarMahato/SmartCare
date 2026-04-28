from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.models.user import User
from app.db.session import SessionLocal
from app.core.security import hash_password
from app.schemas.user import UserLogin
from app.core.security import verify_password, create_access_token
from fastapi import HTTPException
from app.core.security import get_current_user
from fastapi import Depends
from app.models.enums import UserRole
from app.db.dependencies import get_db
router = APIRouter()



@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(
        email=user.email,
        password=hash_password(user.password),
        role=UserRole.patient

    )
    db.add(db_user)
    db.commit()
    return {"message": "User registered successfully"}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid password")

    token = create_access_token({
        "sub": db_user.email,
        "user_id": db_user.id,
        "role": db_user.role
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }
@router.get("/me")
def get_me(current_user: dict = Depends(get_current_user)):
    return {"user": current_user}

