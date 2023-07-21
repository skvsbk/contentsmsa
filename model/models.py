from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy_serializer import SerializerMixin


Base = declarative_base()


class ContentBD(Base, SerializerMixin):
    __tablename__ = 'content'

    id = Column(Integer, primary_key=True)
    userid = Column(Integer)
    title = Column(String(100), nullable=False)
    body = Column(String(255), nullable=False)
