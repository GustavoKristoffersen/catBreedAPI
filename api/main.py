from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm.session import Session

from . import models, schemas
from .database import SessionLocal, engine
from . import crud

from typing import List, Union

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
    "/breeds",
    response_model=Union[List[schemas.CatBreedResponse], schemas.CatBreedResponse],
    status_code=status.HTTP_201_CREATED,
    tags=["Breeds"],
)
async def create(
    request: Union[List[schemas.CatBreedRequest], schemas.CatBreedRequest],
    db: Session = Depends(get_db),
):
    if type(request) == list:
        response_breeds: List[models.Breed] = []

        for breed in request:
            db_breed = crud.create_breed(breed, db=db)
            response_breeds.append(db_breed)

        return response_breeds

    else:
        response = crud.create_breed(request, db=db)

        return response


@app.get(
    "/breeds",
    response_model=List[schemas.CatBreedResponse],
    status_code=status.HTTP_200_OK,
    tags=["Breeds"],
)
async def get_list(
    name: str = None,
    location_of_origin: str = None,
    coat_length: float = None,
    body_type: str = None,
    pattern: str = None,
    db: Session = Depends(get_db),
):
    response = crud.get_breeds_list(db=db)

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


@app.get(
    "/breeds/{id}",
    response_model=schemas.CatBreedResponse,
    status_code=status.HTTP_200_OK,
    tags=["Breeds"],
)
async def get_detail(id: int, db: Session = Depends(get_db)):
    response = crud.get_single_breed(id=id, db=db)

    return response


@app.put(
    "/breeds/{id}",
    response_model=schemas.CatBreedResponse,
    status_code=status.HTTP_200_OK,
    tags=["Breeds"],
)
async def update(id: int, request: schemas.CatBreedUpdate, db: Session = Depends(get_db)):
    response = crud.update_breed(id=id, breed=request, db=db)

    return response


@app.patch(
    "/breeds/{id}",
    response_model=schemas.CatBreedResponse,
    status_code=status.HTTP_200_OK,
    tags=["Breeds"],
)
async def partially_update(id: int, request: schemas.CatBreedUpdate, db: Session = Depends(get_db)):
    response = crud.partially_update_breed(id=id, breed=request, db=db)

    return response


@app.delete("/breeds/{id}", response_model=dict, status_code=status.HTTP_200_OK, tags=["Breeds"])
async def destroy(id: int, db: Session = Depends(get_db)):
    if crud.delete_breed(id=id, db=db):
        return {"message": f"item with id {id} deleted"}
