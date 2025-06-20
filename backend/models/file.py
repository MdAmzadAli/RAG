from sqlalchemy import Column,Integer,String,ForeignKey,DateTime
from sqlalchemy.orm import relationship
from .base import Base
from backend.helper.generate_uuid import generate_uuid
from datetime import datetime,timezone



class File(Base):
    __tablename__="files"
    id=Column(String,primary_key=True,default=generate_uuid)
    filename=Column(String,nullable=False)
    url=Column(String,nullable=False)
    uploaded_at=Column(DateTime,default=datetime.now(timezone.utc))

    user_id=Column(String,ForeignKey("users.id"))
    user=relationship("User",back_populates="files")

    queries=relationship("QueryReply",back_populates="file",cascade="all delete-orphan")