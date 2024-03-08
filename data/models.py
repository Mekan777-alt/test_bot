from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, TIME


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    time_request = Column(TIME, nullable=False)
    article_id = Column(String, unique=True)
