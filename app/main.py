from fastapi import FastAPI

from app.api.endpoints import users, ehr, appointments, allergies, lab_results,ai_transcriptions, medical_history, prescriptions, reminders, followup_recommendations, health_monitoring_logs,ehr_summaries,patient_documents,diagnostic_insights
from app.database.database import engine, Base
from app.config import settings


# Database initialization
Base.metadata.create_all(bind=engine)

# FastAPI instance
app = FastAPI(title="IHMP API", version="1.0")

# Include all routers
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(ehr.router, prefix="/ehr", tags=["EHR"])
app.include_router(appointments.router, prefix="/appointments", tags=["Appointments"])
app.include_router(allergies.router, prefix="/allergy_tracking", tags=["Allergy Tracking"])
app.include_router(lab_results.router, prefix="/lab_results", tags=["Lab Results"])
app.include_router(medical_history.router, prefix="/medical_history", tags=["Medical History"])
app.include_router(prescriptions.router, prefix="/prescriptions", tags=["Prescriptions"])
app.include_router(reminders.router, prefix="/reminders", tags=["Reminders"])
app.include_router(followup_recommendations.router, prefix="/followup", tags=["Follow-Up"])
app.include_router(health_monitoring_logs.router, prefix="/health_monitoring", tags=["Health Monitoring"])
app.include_router(ehr_summaries.router, prefix="/ehrsummary", tags=["Ehr-summary"])
app.include_router(patient_documents.router, prefix="/document", tags=["Patient-document"])
app.include_router(diagnostic_insights.router, prefix="/diagnosis", tags=["Diagnostic_insights"])
app.include_router(ai_transcriptions.router, prefix="/transcriptions", tags=["ai_transcriptions"])

@app.get("/")
def root():
    return {"message": "Welcome to the IHMP API"}
