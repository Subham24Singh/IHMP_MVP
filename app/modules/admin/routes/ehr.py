from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.modules.user.deps import get_current_user
from app.modules.ehr.schema import EHRResponse
from app.modules.ehr.routes import get_ehrs_by_user_id_db, get_ehr_by_id_db
from app.rbac import require_role

admin_ehr_router = APIRouter(
    prefix="/ehr",
    tags=["Admin EHR"],
    dependencies=[Depends(require_role(["Admin"]))]
)

@admin_ehr_router.get("/user/{user_id}", response_model=List[EHRResponse])
def get_user_ehrs(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_ehrs_by_user_id_db(db, user_id)