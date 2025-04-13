from .routes import router as prescriptions
from .models import Prescription
from .schema import (
   PrescriptionSchema
)

__all__ = [
    "prescriptions",
    "Prescription",
    "PrescriptionSchema",
]
