from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy_serializer import SerializerMixin
# from database import engine


Base = declarative_base()


class ContentBD(Base, SerializerMixin):
    __tablename__ = 'content'

    # serialize_only = ('id', 'userid', 'title', 'body')

    id = Column(Integer, primary_key=True)
    userid = Column(Integer)
    title = Column(String(100), nullable=False)
    body = Column(String(255), nullable=False)


    # def as_dict(self):
    #     return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    # def __repr__(self):
    #     # return f'Post(userId={self.userid}, id={self.id}, title={self.title}, body={self.body})'
    #     return str({c.name: getattr(self, c.name) for c in self.__table__.columns})
    #     # return f'"userId": {self.userid}, "id": {self.id}, "title": "{self.title}", "body": "{self.body}"'
    #     # return dict(zip(fruits, prices))

# Base.metadata.create_all(engine)