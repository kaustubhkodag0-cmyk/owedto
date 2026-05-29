from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from database import Base
import datetime

class Commitment(Base):
    __tablename__ = "commitments"
    
    id = Column(Integer, primary_key=True, index=True)
    meeting_title = Column(String, nullable=False)
    owner = Column(String, nullable=False)
    recipient = Column(String, nullable=False)
    deliverable = Column(String, nullable=False)
    deadline = Column(DateTime, nullable=True)
    slack_owner_id = Column(String, nullable=True)
    reminded = Column(Boolean, default=False)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)