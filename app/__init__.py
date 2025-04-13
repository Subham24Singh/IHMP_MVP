# Import key components to make them easily accessible
from .api import router as api_router
from .models import (
    User, EHR, Appointment, AllergyTracking, LabResults, MedicalHistory,
    Prescription, Reminder, PatientUploadedDocs,
    DiagnosticInsights, EHRSummary, FollowupRecommendations, HealthMonitoringLogs
)
from .schemas import (
    UserSchema, EHRSchema, AppointmentCreate, AppointmentResponse,
    AllergyTrackingCreate, AllergyTrackingResponse, LabResultSchema,
    MedicalHistorySchema, PrescriptionSchema, ReminderSchema,
    PatientUploadedDocsSchema, AITranscriptionsSchema, DiagnosticInsightsSchema,
    EHRSummarySchema, FollowupRecommendationsSchema, HealthMonitoringLogsSchema
)
from app.database.database import SessionLocal, engine, Base