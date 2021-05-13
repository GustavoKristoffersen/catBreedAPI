from pydantic import BaseModel, Field


class CatBreed(BaseModel):
    id: int = None
    name: str = Field(max_length=50)
    location_of_origin: str
    coat_length: float = Field(gt=0)
    body_type: str
    pattern: str

    class Config:
        orm_mode = True
