from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
# from database import engine


Base = declarative_base()


class ContentBD(Base):
    __tablename__ = 'content'

    id = Column(Integer, primary_key=True)
    userid = Column(Integer)
    title = Column(String(100), nullable=False)
    body = Column(String(255), nullable=False)

    def __repr__(self):
        return f'Post(userId={self.userid}, id={self.id}, title={self.title}, body={self.body})'

# Base.metadata.create_all(engine)