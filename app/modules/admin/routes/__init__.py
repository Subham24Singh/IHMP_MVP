from .ai_transcription import admin_ai_transcription_router
from .ehr_summary import admin_ehr_summary_router
from .appointments import admin_appointments_router
from .lab_results import admin_lab_results_router
from .reminder import admin_reminder_router
from .followup import admin_follow_up_router
from .profile import admin_profile_router
from .prescription import admin_prescription_router 
from .ehr import admin_ehr_router

routers = [
    admin_ai_transcription_router,
    admin_ehr_summary_router,
    admin_appointments_router,
    admin_lab_results_router,
    admin_reminder_router,
    admin_follow_up_router,
    admin_profile_router,
    admin_prescription_router,
    admin_ehr_router

]