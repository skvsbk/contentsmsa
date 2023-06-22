from sqlalchemy.orm import Session
from models import ContentBD


def get_all_posts(db: Session):
    query = db.query(ContentBD).all()
    return query

def get_posts_by_author(db: Session, value):
    query = db.query(ContentBD).filter(userid=value.userid).all()
    return query

def get_post_by_author(db: Session, value):
    query = db.query(ContentBD).filter(userid=value.userid, id=value.id).one()
    return query


def create_post(db: Session, value):
    query = ContentBD(userid=value.userid, title=value.title, body=value.body)
    db.add(query)
    db.commit()
    db.refresh(query)
    return query

def update_post(db: Session, value):
    query = db.query(ContentBD).filter(userid=value.userid, id=value.id).one()
    query.title = value.title
    query.body = value.body
    db.commit()
    db.refresh(query)
    return query


def delete_post(db: Session, value):
    query = db.query(ContentBD).filter(id=value.id).one()
    db.delete(query)
    return "{'result': 'post deleted'}"
