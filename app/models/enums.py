import enum

class RoleEnum(str, enum.Enum):
    Doctor = "Doctor"
    Patient = "Patient"
    Admin = "Admin"

class StatusEnum(str, enum.Enum):
    Scheduled = "Scheduled"
    Completed = "Completed"
    Cancelled = "Cancelled"