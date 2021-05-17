from fastapi import status, HTTPException
from sqlalchemy.orm import Session

from . import schemas
from . import models


def create_breed(breed: schemas.CatBreedRequest, db: Session):
    '''
    Creates a new breed in the database.
    '''

    if db.query(models.Breed).filter_by(name=breed.name).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Breed with this name already exists",
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

    return new_breed


def get_breeds_list(db: Session):
    '''
    Returns all breeds in the database
    '''

    return db.query(models.Breed)


def get_single_breed(id: int, db: Session):
    '''
    returns a single breed from the database.
    '''

    db_breed = db.query(models.Breed).filter_by(id=id).first()
    if not db_breed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Breed with id {id} does not exist",
        )

    return db_breed


def update_breed(id: int, breed: schemas.CatBreedUpdate, db: Session):
    '''
    Updates a single breed in the database.
    '''

    db_breed = db.query(models.Breed).filter_by(id=id)

    if not db_breed.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Breed with id {id} does not exist",
        )

    check = db.query(models.Breed).filter_by(name=breed.name).first()
    if check and check != db_breed.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Breed with this name already exists",
        )

    db_breed.update(breed.dict())
    db.commit()

    return db.query(models.Breed).filter_by(id=id).first()


def partially_update_breed(id: int, breed: schemas.CatBreedUpdate, db: Session):
    '''
    Partially updates a single breed in the database.
    You can pass only the data you want to update.
    e.g. {'name': 'new name"}
    '''

    db_breed = db.query(models.Breed).filter_by(id=id)

    if not db_breed.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Breed with id {id} does not exist",
        )

    if breed.name:
        check = db.query(models.Breed).filter_by(name=breed.name).first()
        if check and check != db_breed.first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Breed with this name already exists",
            )

    db_breed.update(breed.dict(exclude_unset=True))
    db.commit()
    
    return db.query(models.Breed).filter_by(id=id).first()


def delete_breed(id: int, db: Session):
    '''
    Deletes a single breed from the database.
    '''

    db_breed = db.query(models.Breed).filter_by(id=id).first()

    if not db_breed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Breed with id {id} does not exist",
        )

    db.delete(db_breed)
    db.commit()

    return True
