from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.modules.user.deps import get_current_user
from app.modules.labresults.schema import LabResultCreate, LabResultResponse
from app.modules.labresults.routes import (
    create_lab_result_db,
    get_lab_results_by_user_id_db,
    get_lab_result_by_id_db,
    update_lab_result_db,
    delete_lab_result_db,
)
from app.rbac import require_role

admin_lab_results_router = APIRouter(
    prefix="/labresults",
    tags=["Admin Lab Results"],
    dependencies=[Depends(require_role(["Admin"]))]
)

@admin_lab_results_router.post("/", response_model=LabResultResponse)
def admin_create_lab_result(
    lab_result_data: LabResultCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return create_lab_result_db(db, lab_result_data)

@admin_lab_results_router.get("/user/{user_id}", response_model=List[LabResultResponse])
def admin_get_lab_results_by_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_lab_results_by_user_id_db(db, user_id)

@admin_lab_results_router.put("/{lab_result_id}", response_model=LabResultResponse)
def admin_update_lab_result(
    lab_result_id: int,
    lab_result_data: LabResultCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    updated = update_lab_result_db(db, lab_result_id, lab_result_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Lab result not found.")
    return updated

@admin_lab_results_router.delete("/{lab_result_id}", status_code=204)
def admin_delete_lab_result(
    lab_result_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    success = delete_lab_result_db(db, lab_result_id)
    if not success:
        raise HTTPException(status_code=404, detail="Lab result not found.")
    return