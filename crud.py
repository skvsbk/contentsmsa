from models import ContentBD
from database import SessionLocal
from serializers import serializer_posts, serializer_posts_without_userid


# 2
def get_all_posts():
    """
    Get all posts ordered by id from DB
    :return: list of dicts
    """
    with SessionLocal() as session:
        query = session.query(ContentBD).order_by(ContentBD.id)
    return [serializer_posts(item.to_dict()) for item in query]


# 3
def get_posts_by_author(user_id):
    """
    Get posts by user_id from DB
    :param user_id: int
    :return: list of dicts
    """
    with SessionLocal() as session:
        query = session.query(ContentBD).filter(ContentBD.userid == user_id).all()
    return [serializer_posts_without_userid(item.to_dict()) for item in query]


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


# 5
def get_all_posts_ordered_by_userid():
    """
    Get all posts ordered by id from DB
    :return: list of dicts
    """
    with SessionLocal() as session:
        query = session.query(ContentBD).order_by(ContentBD.userid)
    return [serializer_posts(item.to_dict()) for item in query]


def create_post(value):
    """
    Create post with param
    :param value: dict {'user_id': 1, 'titte': 'post titte', 'body': 'post body'}
    :return: dict of received input values, but padded with the id key
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


def update_post(value):
    """
    Update post with userid and post id
    :param value: dict {'user_id': 1, 'titte': 'post titte', 'body': 'post body'}
    :return: dict of received input values, but padded with the id key
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
