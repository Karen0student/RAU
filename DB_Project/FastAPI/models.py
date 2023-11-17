from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base
import session as _session

Base = declarative_base()

class Todo(Base):
    __tablename__ = "actor"

    id = Column(Integer, primary_key=True)
    # models.ForeignKey("app.Model", verbose_name=_(""), on_delete=models.CASCADE)
    text = Column(String)
    is_done = Column(Boolean, default=False)
    


Base.metadata.create_all(_session.engine)