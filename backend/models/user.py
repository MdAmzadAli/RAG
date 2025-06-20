from sqlalchemy import Column,Integer,String,Boolean
from sqlalchemy.orm import relationship
from .base import Base
from backend.helper.generate_uuid import generate_uuid



class User(Base):
    __tablename__ = "users"
    id=Column(String,primary_key=True,default=generate_uuid)
    email=Column(String,unique=True,nullable=False)
    password=Column(String,nullable=False)
    files=relationship("File",back_populates="user",cascade="all delete-orphan")