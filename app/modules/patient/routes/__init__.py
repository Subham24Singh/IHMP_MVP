from .ai_transcriptions import patient_ai_transcription_router
from .ehr_summary import patient_ehr_summary_router
from .appointments import patient_appointments_router
from .lab_results import patient_lab_results_router 
from .allergy_tracking import patient_allergy_tracking_router
from .reminder import patient_reminder_router
from .followup import patient_follow_up_router
from .profile import patient_profile_router
from .prescription import patient_prescription_router
from .ehr import patient_ehr_router

routers = [
    patient_ai_transcription_router,
    patient_ehr_summary_router,
    patient_appointments_router,
    patient_lab_results_router,
    patient_allergy_tracking_router,
    patient_reminder_router,
    patient_follow_up_router,
    patient_profile_router,
    patient_prescription_router,
    patient_ehr_router
]