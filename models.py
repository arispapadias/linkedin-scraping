from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()

class JobModel(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    job_title = Column(String, index=True)
    company_name = Column(String)
    company_location = Column(String)
    job_description = Column(Text)

class Jobs(BaseModel):
    job_title: str
    company_name: str
    company_location: str
    job_description: str
