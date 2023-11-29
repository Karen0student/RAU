from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Date
from sqlalchemy.orm import declarative_base # , relationship, backref
# import FastAPI.session as _session
# from datetime import datetime, date
import subprocess

Base = declarative_base()

class actor(Base):
    __tablename__ = "actor"

    id = Column(Integer, primary_key=True, nullable=False)
    Name_Surname = Column(String(50), nullable=False, index=True) # to find faster, EATING RAM
    rank = Column(String(20), nullable=True)
    age = Column(Integer, nullable=False)
    gender = Column(String(10), nullable=True)
    ampula = Column(String(20), nullable=True)

class postanovka(Base):
    __tablename__ = "postanovka"
    
    id = Column(Integer, ForeignKey("actor.id"), primary_key=True, nullable=False)
    start_role = Column(Date)
    stop_role = Column(Date)
    role_type = Column(String(20), nullable=True)
    group_number = Column(Integer, nullable=False)
    director = Column(String(20), nullable=False)
    date_of = Column(Date)
    
    
class role(Base):
    __tablename__ = "role"
    
    id = Column(Integer, ForeignKey("actor.id"), primary_key=True, nullable=False)
    name = Column(String(20), nullable=False)
    ampula = Column(String(20), nullable=True)
    piesa = Column(String(20), nullable=True)
    gender = Column(String(10), nullable=True)
    
    
# Base.metadata.create_all(_session.engine)

# # ADDING VALUES INTO TABLES
# with open("/home/voyager/Visual_Studio/DB_Project/FastAPI/insert_values_into_db.py", 'r') as input_file:
#     exec(input_file.read())
