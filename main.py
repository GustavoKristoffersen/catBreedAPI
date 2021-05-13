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


@app.get(
    "/breeds", response_model=List[schemas.CatBreed], status_code=200, tags=["Breeds"]
)
async def get_list(
    name: str = None,
    location_of_origin: str = None,
    coat_length: float = None,
    body_type: str = None,
    pattern: str = None,
    db: Session = Depends(get_db),
):
    response = db.query(models.Breed)

    if name:
        response = response.filter_by(name=name)
    if location_of_origin:
        response = response.filter_by(location_of_origin=location_of_origin)
    if coat_length:
        response = response.filter_by(coat_length=coat_length)
    if body_type:
        response = response.filter_by(body_type=body_type)
    if pattern:
        response = response.filter_by(pattern=pattern)
    
    return response.all()

@app.get('/breeds/{id}', response_model=schemas.CatBreed, status_code=200, tags=['Breeds'])
async def get_detail(id: int, db: Session = Depends(get_db)):
    response = db.query(models.Breed).filter_by(id=id).first()
    if not response:
        raise HTTPException(status_code=404, detail=f"Breed with id {id} does not exist")
    return response