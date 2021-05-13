from fastapi import FastAPI, HTTPException, Depends
from pydantic.networks import HttpUrl
from sqlalchemy.orm import Session

import models, schemas
from database import SessionLocal, engine

from typing import List


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post(
    "/breeds", response_model=List[schemas.CatBreed], status_code=201, tags=["Breeds"]
)
async def create(request: List[schemas.CatBreed], db: Session = Depends(get_db)):  
    response_breeds: List[models.Breed] = []

    for breed in request:
        if db.query(models.Breed).filter_by(name=breed.name).first():
            raise HTTPException(
                status_code=400, detail="Breed with this name already exists"
            )

        new_breed = models.Breed(
            name=breed.name,
            location_of_origin=breed.location_of_origin,
            coat_length=breed.coat_length,
            body_type=breed.body_type,
            pattern=breed.pattern,
        )

        db.add(new_breed)
        db.commit()

        response_breeds.append(new_breed)

    return response_breeds
