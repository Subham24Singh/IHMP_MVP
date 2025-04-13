from .routes import router as patient_uploaded_doc
from .models import PatientUploadedDocs
from .schema import (
   PatientUploadedDocsSchema
)

__all__ = [
    "patient_uploaded_doc",
    "PatientUploadedDocs",
    "PatientUploadedDocsSchema",
]
