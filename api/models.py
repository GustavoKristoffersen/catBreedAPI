from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.sql.schema import CheckConstraint

from .database import Base


class Breed(Base):
    __tablename__ = "breed"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    location_of_origin = Column(String)
    coat_length = Column(String) #Salvo como String devido à limitações do sqlite
    body_type = Column(String)
    pattern = Column(String)
