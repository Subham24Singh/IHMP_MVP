from .routes import router as lab_results
from .model import LabResults
from .schema import (
   LabResultSchema
)

__all__ = [
    "lab_results",
    "LabResults",
    "LabResultSchema",
    
]
