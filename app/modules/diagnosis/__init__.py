

from .routes import router as diagnostic_insight_router
from .model import DiagnosticInsights
from .schema import (
   DiagnosticInsightsSchema
)

__all__ = [
    "diagnostic_insight_router",
    "DiagnosticInsights",
    "DiagnosticInsightsSchema",
    
]
