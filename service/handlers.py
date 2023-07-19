from abc import ABC, abstractmethod
from model.models import ContentBD
from model.database import SessionLocal
from service.serializers import UserPostsSerializer, PostsWOUseridSerializer, PostsSerializer, UserPostsListSerializer


class Handler(ABC):
    @abstractmethod
    def produce(self, request):
        pass


class GetAllPosts(Handler):
    def produce(self, request=None):
        """
        Get all posts ordered by id from DB
        :return: list of dicts
        """
        with SessionLocal() as session:
            query = session.query(ContentBD).order_by(ContentBD.id)
        return [PostsSerializer(item.to_dict()).data() for item in query]


class CreatePost(Handler):
    def produce(self, request):
        """
        Create post with param
        :param request: dict {"user_id": 1, "title": "post title", "body': "post body"}
        :return: dict of received input values, but padded with the id key
        """
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
    def produce(self, request):
        """
        Get posts by user_id from DB
        :param request: dict
        :return: list of dicts
        """
        with SessionLocal() as session:
            query = session.query(ContentBD).filter(ContentBD.userid == request["user_id"]).all()

        posts = [PostsWOUseridSerializer(item.to_dict()).data() for item in query]
        user_data = request["user_data"]

        return UserPostsSerializer(user_data, posts).data()


class GetPostById(Handler):
    def produce(self, request):
        """
        Get post by post_id from DB
        :param request: dict
        :return: dict
        """
        with SessionLocal() as session:
            query = session.query(ContentBD).filter(ContentBD.id == request["post_id"]).all()
            if len(query) == 0:
                return {'detail': 'Not found'}
            else:
                return query[0].to_dict()


class UpdatePost(Handler):
    def produce(self, request):
        """
        Update post with userid and post id
        :param request: dict {'user_id': 1, 'id': 10, 'titte': 'post titte', 'body': 'post body'}
        :return: dict of received input values, but padded with the id key
        """
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
    def produce(self, request):
        """
        Delete post with post_id
        :param request: dict
        :return: dict
        """
        try:
            with SessionLocal() as session:
                query = session.query(ContentBD).filter(ContentBD.id == request["post_id"]).one()
                session.delete(query)
                session.commit()
            return {'detail': 'Post has been deleted'}
        except:
            return {'detail': 'Post is not found'}


class GetAllPostsOrderedByUserId(Handler):
    def produce(self, request):
        """
        Get all posts ordered by id from DB
        :return: list of dicts
        """
        with SessionLocal() as session:
            query = session.query(ContentBD).order_by(ContentBD.userid)

        posts = [PostsSerializer(item.to_dict()).data() for item in query]
        user_data = request["user_data"]
        return UserPostsListSerializer(user_data, posts).data()
