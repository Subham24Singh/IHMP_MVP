from fastapi import APIRouter
from app.api.endpoints import (
    users, 
    ehr, 
    appointments, 
    allergies, 
    lab_results, 
    medical_history, 
    prescriptions, 
    reminders,
    patient_documents,
    ehr_summaries,
    followup_recommendations,
    health_monitoring_logs
)

router = APIRouter()

# Include routers from all endpoint modules
router.include_router(users.router)
router.include_router(ehr.router)
router.include_router(appointments.router)
router.include_router(allergies.router)
router.include_router(lab_results.router)
router.include_router(medical_history.router)
router.include_router(prescriptions.router)
router.include_router(reminders.router)
router.include_router(patient_documents.router)
router.include_router(ehr_summaries.router)
router.include_router(followup_recommendations.router)
router.include_router(health_monitoring_logs.router)