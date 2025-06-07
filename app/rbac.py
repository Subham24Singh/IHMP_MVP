from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.modules.user.auth import decode_access_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def require_role(allowed_roles):
    def role_checker(token: str = Depends(oauth2_scheme)):
        payload = decode_access_token(token)
        role = payload.get("role")
        if role not in allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
        return payload
    return role_checker 