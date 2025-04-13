from pydantic import BaseModel

class AllergyTrackingCreate(BaseModel):
    user_id: int
    allergy_name: str
    reaction: str

class AllergyTrackingResponse(BaseModel):
    allergy_id: int
    user_id: int
    allergy_name: str
    reaction: str

    class Config:
        orm_mode = True