# app/modules/users/deps.py
from fastapi import Depends, HTTPException
from app.modules.user.auth import decode_access_token
from fastapi.security import OAuth2PasswordBearer  # Import OAuth2PasswordBearer
from app.modules.user.model import User
from app.database.database import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    user_id = payload.get("sub")
    db = SessionLocal()
    user = db.query(User).filter(User.user_id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

def require_role(role: str):
    def role_checker(user=Depends(get_current_user)):
        if user.role != role:
            raise HTTPException(status_code=403, detail="Access forbidden")
        return user
    return role_checker


from fastapi import Depends, HTTPException, status
from app.modules.user.model import User
from app.modules.user.deps import get_current_user  # Assuming you already have this

def get_current_patient(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "Patient":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only patients can access this resource."
        )
    return current_user