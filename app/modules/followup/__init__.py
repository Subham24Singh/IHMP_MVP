from .routes import router as follow_up_router
from .model import FollowupRecommendations
from .schema import (
   FollowupRecommendationsSchema
)

__all__ = [
    "FollowupRecommendations",
    "FollowupRecommendationsSchema",
    "follow_up_router",
    
]
