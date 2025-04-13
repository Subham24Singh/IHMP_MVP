from pydantic import BaseModel

class LabResultSchema(BaseModel):
    user_id: int
    test_name: str
    result_data: str

    class Config:
        orm_mode = True