from fastapi import FastAPI

from app.database.database import engine, Base
from app.config import settings

# Import modules

from app.modules import (
    user,
    appointment,
    allergytracking,
    labresults,
    ai_transcription,
    medical_history,
    prescription,
    reminder,
    followup,
    healthmonitoring,
    ehrsummary,
    patient_uploaded_docs,
    ehr,
    diagnosis
)

# DB init
Base.metadata.create_all(bind=engine)

app = FastAPI(title="IHMP API", version="1.0")

# Use correct router names
app.include_router(user.user_router, prefix="/users", tags=["Users"])
app.include_router(ehr.ehr_router, prefix="/ehr", tags=["EHR"])
app.include_router(appointment.appointments_router, prefix="/appointments", tags=["Appointments"])
app.include_router(allergytracking.allergy_tracking_router, prefix="/allergy_tracking", tags=["Allergy Tracking"])
app.include_router(labresults.lab_results, prefix="/lab_results", tags=["Lab Results"])
app.include_router(medical_history.medical_history, prefix="/medical_history", tags=["Medical History"])
app.include_router(prescription.prescriptions, prefix="/prescriptions", tags=["Prescriptions"])
app.include_router(reminder.reminder, prefix="/reminders", tags=["Reminders"])
app.include_router(followup.follow_up_router, prefix="/followup", tags=["Follow-Up"])
app.include_router(healthmonitoring.health_monitoring_log, prefix="/health_monitoring", tags=["Health Monitoring"])
app.include_router(ehrsummary.ehr_summary_router, prefix="/ehrsummary", tags=["EHR Summary"])
app.include_router(patient_uploaded_docs.patient_uploaded_doc, prefix="/document", tags=["Patient Document"])
app.include_router(diagnosis.diagnostic_insight_router, prefix="/diagnosis", tags=["Diagnostic Insights"])
app.include_router(ai_transcription.ai_transcription_router, prefix="/transcriptions", tags=["AI Transcriptions"])

@app.get("/")
def root():
    return {"message": "Welcome to the IHMP API"}
