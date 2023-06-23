from models import ContentBD
from database import SessionLocal


def get_all_posts(): # 2
    with SessionLocal() as session:
        query = session.query(ContentBD).all()
    return query

def get_posts_by_author(user_id): # 3
    with SessionLocal() as session:
        query = session.query(ContentBD).filter(ContentBD.userid == user_id).all()
    return query

def get_post_by_id(post_id): # 4
    with SessionLocal() as session:
        query = session.query(ContentBD).filter(ContentBD.id == post_id).one()
    return query


def create_post(value):
    with SessionLocal() as session:
        query = ContentBD(userid=value.user_id,
                          title=value.title,
                          body=value.body)
        session.add(query)
        session.commit()
        session.refresh(query)
    return query

def update_post(value):
    with SessionLocal() as session:
        query = session.query(ContentBD).filter(ContentBD.userid == value.userid,
                                                ContentBD.id == value.id).one()
        query.title = value.title
        query.body = value.body
        session.commit()
        session.refresh(query)
    return query


def delete_post(post_id):
    with SessionLocal() as session:
        query = session.query(ContentBD).filter(ContentBD.id == post_id).one()
        session.delete(query)
    return "{'details': 'post deleted'}"
