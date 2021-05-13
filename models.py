from sqlalchemy import Column, Integer, String, Numeric

from database import Base


class Breed(Base):
    __tablename__ = "breeds"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    location_of_origin = Column(String)
    coat_length = Column(Numeric)
    body_type = Column(String)
    pattern = Column(String)
