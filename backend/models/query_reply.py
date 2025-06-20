from sqlalchemy import Column,String,ForeignKey,DateTime,Text
from sqlalchemy.orm import relationship
from .base import Base
from backend.helper.generate_uuid import generate_uuid
from datetime import datetime,timezone


class QueryReply(Base):
    __tablename__ = "query_replies"

    id = Column(String, primary_key=True, default=generate_uuid)
    query = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    file_id = Column(String, ForeignKey("files.id"))
    file = relationship("File", back_populates="queries")