from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base # , relationship, backref

Base = declarative_base()

class alembic_created(Base):
    __tablename__ = "alembic_created_actor"

    id = Column(Integer, primary_key=True, nullable=False)
    Name_Surname = Column(String(50), nullable=False)
    rank = Column(String(20), nullable=True)
    age = Column(Integer, nullable=False)
    gender = Column(String(10), nullable=True)
    ampula = Column(String(20), nullable=True)


class alembic_created_role(Base):
    __tablename__ = "alembic_created_role"
    id = Column(Integer, ForeignKey("alembic_created_actor.id"), primary_key=True, nullable=False)
    name = Column(String(20), nullable=False)
    ampula = Column(String(20), nullable=True)
    piesa = Column(String(20), nullable=True)
    gender = Column(String(10), nullable=True)

    