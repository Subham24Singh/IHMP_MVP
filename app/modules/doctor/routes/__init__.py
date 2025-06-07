from .ai_transcription import doctor_ai_transcription_router
from .ehr_summary import doctor_ehr_summary_router
from .appointments import doctor_appointments_router
from .lab_results import doctor_lab_results_router
from .reminder import doctor_reminder_router
from .followup import doctor_follow_up_router
from .profile import doctor_profile_router
from .prescription import doctor_prescription_router
from .ehr import doctor_ehr_router


routers = [
    doctor_ai_transcription_router,
    doctor_ehr_summary_router,
    doctor_appointments_router,
    doctor_lab_results_router,
    doctor_reminder_router,
    doctor_follow_up_router,
    doctor_profile_router,
    doctor_prescription_router,
    doctor_ehr_router
]