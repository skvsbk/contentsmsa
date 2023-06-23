from models import ContentBD
from database import SessionLocal


# 2
def get_all_posts():
    """
    Get all posts from DB
    :return: list of dicts
    """
    with SessionLocal() as session:
        query = session.query(ContentBD).all()
    return [item.to_dict() for item in query]


# 3
def get_posts_by_author(user_id):
    """
    Get posts by userid from DB
    :param user_id: int
    :return: list of dicts
    """
    with SessionLocal() as session:
        query = session.query(ContentBD).filter(ContentBD.userid == user_id).all()
    return [item.to_dict() for item in query]


# 4
def get_post_by_id(post_id):
    """
    Get post by post_id from DB
    :param post_id: int
    :return: dict
    """
    with SessionLocal() as session:
        query = session.query(ContentBD).filter(ContentBD.id == post_id).all()
        if len(query) == 0:
            return {'details': 'Not found'}
        else:
            return query[0].to_dict()


def create_post(value):
    """

    :param value: dict {'user_id': 1, 'titte': 'some titte', 'body': 'some body'}
    :return: dict like value, but additional with id
    """
    try:
        with SessionLocal() as session:
            query = ContentBD(userid=value['user_id'],
                              title=value['title'],
                              body=value['body'])
            session.add(query)
            session.commit()
            session.refresh(query)
        return query.to_dict()
    except:
        return {'details': 'Post was not created'}


def update_post(value, ):
    """
    Update post by
    :param value: dict {'user_id': 1, 'titte': 'some titte', 'body': 'some body'}
    :return: dict like value, but additional with id
    """
    try:
        with SessionLocal() as session:
            query = session.query(ContentBD).filter(ContentBD.userid == value['user_id'],
                                                    ContentBD.id == value['id']).one()
            query.title = value['title']
            query.body = value['body']
            session.commit()
            session.refresh(query)
        return query.to_dict()
    except:
        return {'details': 'Can not update post'}


def delete_post(post_id):
    """
    Delete post with post_id
    :param post_id: int
    :return: dict
    """
    try:
        with SessionLocal() as session:
            query = session.query(ContentBD).filter(ContentBD.id == post_id).one()
            session.delete(query)
            session.commit()
        return {'details': 'Post deleted'}
    except:
        return {'details': 'Post is not found'}
