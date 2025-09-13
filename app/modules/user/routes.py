from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.modules.user.deps import get_current_user
from app.modules.user.model import User
from app.modules.user.auth import get_password_hash, verify_password, create_access_token
from app.modules.user.schema import PatientRegisterInput, DoctorRegisterInput, UserOutputSchema
from app.database.database import SessionLocal
from app.modules.enum.models import RoleEnum
import traceback

user_router = APIRouter(tags=["Users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@user_router.post("/register_patient", response_model=UserOutputSchema)
def register_patient(patient_data: PatientRegisterInput, db: Session = Depends(get_db)):
    try:
        if db.query(User).filter(User.email == patient_data.email).first():
            raise HTTPException(status_code=400, detail="Email already exists")
        if db.query(User).filter(User.phone_number == patient_data.phone_number).first():
            raise HTTPException(status_code=400, detail="Phone number already exists")
        if patient_data.password != patient_data.confirm_password:
            raise HTTPException(status_code=400, detail="Passwords do not match")
        hashed_pwd = get_password_hash(patient_data.password)
        new_user = User(
            username=patient_data.username,
            email=patient_data.email,
            hashed_password=hashed_pwd,
            phone_number=patient_data.phone_number,
            role=RoleEnum.Patient
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return UserOutputSchema.from_orm(new_user)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

@user_router.post("/register_doctor", response_model=UserOutputSchema)
def register_doctor(doctor_data: DoctorRegisterInput, db: Session = Depends(get_db)):
    try:
        if db.query(User).filter(User.email == doctor_data.email).first():
            raise HTTPException(status_code=400, detail="Email already exists")
        if db.query(User).filter(User.phone_number == doctor_data.phone_number).first():
            raise HTTPException(status_code=400, detail="Phone number already exists")
        if doctor_data.password != doctor_data.confirm_password:
            raise HTTPException(status_code=400, detail="Passwords do not match")
        # CRITICAL: Validate registration_number (implement your logic here)
        if not doctor_data.registration_number or len(doctor_data.registration_number) < 5:
            raise HTTPException(status_code=400, detail="Invalid registration number")
        hashed_pwd = get_password_hash(doctor_data.password)
        new_user = User(
            username=doctor_data.username,
            email=doctor_data.email,
            hashed_password=hashed_pwd,
            phone_number=doctor_data.phone_number,
            role=RoleEnum.Doctor,
            registration_number=doctor_data.registration_number
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return UserOutputSchema.from_orm(new_user)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")


@user_router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.email == form_data.username).first()
        if not user or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
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

@user_router.get("/profile", response_model=UserOutputSchema)
def get_profile(current_user: User = Depends(get_current_user)):
    return UserOutputSchema.from_orm(current_user)