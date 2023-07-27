from abc import ABC, abstractmethod

from model.models import ContentBD
from model.database import SessionLocal
from service.serializers import UserPostsSerializer, PostsWOUseridSerializer, PostsSerializer, UserPostsListSerializer
from service import result_submission_publisher
from config import Config


class DefineHandler:
    """Selecting a handler based on a request and then sending the results"""

    def __init__(self, request, key):
        self.request = request
        self.key = key

    def execute_handler(self):
        if self.request["name"] not in Config.AVAILABLE_REQUESTS:
            result = {'detail': 'No handler for request'}
            result_submission_publisher.change_state(key=self.key, value=result)
            return

        match self.request["name"]:
            # 2
            case 'get_posts_list':
                match self.request['method']:
                    case 'get':
                        result = GetAllPosts().execute()
                        result_submission_publisher.change_state(key=self.key, value=result)
                    case 'post':
                        result = CreatePost().execute(self.request)
                        result_submission_publisher.change_state(key=self.key, value=result)
            # 3
            case 'get_authors_id_posts_list':
                result = GetPostsByAuthor().execute(self.request)
                result_submission_publisher.change_state(key=self.key, value=result)
            # 4
            case 'get_posts_id':
                match self.request['method']:
                    case 'get':
                        result = GetPostById().execute(self.request)
                        result_submission_publisher.change_state(key=self.key, value=result)
                    case 'put':
                        result = UpdatePost().execute(self.request)
                        result_submission_publisher.change_state(key=self.key, value=result)
                    case 'delete':
                        result = DeletePost().execute(self.request)
                        result_submission_publisher.change_state(key=self.key, value=result)
            # 5
            case 'get_posts_with_authors_list':
                result = GetAllPostsOrderedByUserId().execute(self.request)
                result_submission_publisher.change_state(key=self.key, value=result)


class Handler(ABC):
    """Interface for concrete handlers"""
    @abstractmethod
    def execute(self, request):
        pass


class GetAllPosts(Handler):
    """
    Get all posts ordered by id from DB
    :return: list of dicts
    """

    def execute(self, request=None):
        with SessionLocal() as session:
            query = session.query(ContentBD).order_by(ContentBD.id)
        return [PostsSerializer(item.to_dict()).data() for item in query]


class CreatePost(Handler):
    """
    Create post with param
    :param request: dict {"user_id": 1, "title": "post title", "body": "post body"}
    :return: dict of received input values, but padded with the id key
    """

    def execute(self, request):
        try:
            with SessionLocal() as session:
                query = ContentBD(userid=request['user_id'],
                                  title=request['title'],
                                  body=request['body'])
                session.add(query)
                session.commit()
                session.refresh(query)
            return query.to_dict()
        except:
            return {'detail': 'Post was not created'}


class GetPostsByAuthor(Handler):
    """
    Get posts by user_id from DB
    :param request: dict
    :return: list of dicts
    """

    def execute(self, request):
        with SessionLocal() as session:
            query = session.query(ContentBD).filter(ContentBD.userid == request["user_id"]).all()

        posts = [PostsWOUseridSerializer(item.to_dict()).data() for item in query]
        user_data = request["user_data"]

        return UserPostsSerializer(user_data, posts).data()


class GetPostById(Handler):
    """
    Get post by post_id from DB
    :param request: dict
    :return: dict
    """

    def execute(self, request):
        with SessionLocal() as session:
            query = session.query(ContentBD).filter(ContentBD.id == request["post_id"]).all()
            if len(query) == 0:
                return {'detail': 'Not found'}
            else:
                return query[0].to_dict()


class UpdatePost(Handler):
    """
    Update post with userid and post id
    :param request: dict {'user_id': 1, 'id': 10, 'titte': 'post titte', 'body': 'post body'}
    :return: dict of received input values, but padded with the id key
    """

    def execute(self, request):
        try:
            with SessionLocal() as session:
                query = session.query(ContentBD).filter(ContentBD.userid == request['user_id'],
                                                        ContentBD.id == request['id']).one()
                query.title = request['title']
                query.body = request['body']
                session.commit()
                session.refresh(query)
            return query.to_dict()
        except:
            return {'detail': 'Can not update post'}


class DeletePost(Handler):
    """
    Delete post with post_id
    :param request: dict
    :return: dict
    """

    def execute(self, request):
        try:
            with SessionLocal() as session:
                query = session.query(ContentBD).filter(ContentBD.id == request["post_id"]).one()
                session.delete(query)
                session.commit()
            return {'detail': 'Post has been deleted'}
        except:
            return {'detail': 'Post is not found'}


class GetAllPostsOrderedByUserId(Handler):
    """
    Get all posts ordered by id from DB
    :return: list of dicts
    """

    def execute(self, request):
        with SessionLocal() as session:
            query = session.query(ContentBD).order_by(ContentBD.userid)

        posts = [PostsSerializer(item.to_dict()).data() for item in query]
        user_data = request["user_data"]
        return UserPostsListSerializer(user_data, posts).data()
