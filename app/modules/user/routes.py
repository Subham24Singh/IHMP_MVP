# app/modules/users/routes.py
from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.modules.user.deps import get_current_user
from app.modules.user.model import User
from app.modules.user.auth import get_password_hash, verify_password, create_access_token
from app.modules.user.schema import UserSchema
from app.database.database import SessionLocal
from app.modules.enum.models import RoleEnum
import traceback

user_router = APIRouter(tags=["Users"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@user_router.post("/register")
def register(user_data: UserSchema, db: Session = Depends(get_db)):
    try:
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already exists")
        existing_phone = db.query(User).filter(User.phone_number == user_data.phone_number).first()
        if existing_phone:
            raise HTTPException(status_code=400, detail="Phone number already exists")
        # Convert role string to RoleEnum (case-insensitive)
        role_clean = user_data.role.strip().lower()
        role_map = {r.value.lower(): r for r in RoleEnum}
        if role_clean not in role_map:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid role: {user_data.role}. Must be one of {[r.value for r in RoleEnum]}"
            )
        role_enum = role_map[role_clean]
        hashed_pwd = get_password_hash(user_data.password)
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_pwd,
            phone_number=user_data.phone_number,
            role=role_enum
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {
            "user_id": new_user.user_id,
            "username": new_user.username,
            "email": new_user.email,
            "role": new_user.role.value,
            "message": "User registered successfully"
        }
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

@user_router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.email == form_data.username).first()
        if not user or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Invalid credentials")
        token = create_access_token(data={"sub": str(user.user_id), "role": user.role.value})
        return {
            "access_token": token,
            "token_type": "bearer",
            "user_id": user.user_id,
            "username": user.username,
            "email": user.email,
            "role": user.role.value
        }
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")

@user_router.get("/profile")
def get_profile(current_user: User = Depends(get_current_user)):
    return {
        "user_id": current_user.user_id,
        "username": current_user.username,
        "email": current_user.email,
        "phone_number": current_user.phone_number,
        "role": current_user.role.value
    }

