from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, DateTime, String, func, TIME
from datetime import datetime


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    time_request = Column(TIME, default=datetime.now().time())
    article_id = Column(String, unique=True)
    next_message = Column(TIME, nullable=True)
