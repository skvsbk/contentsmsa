class PostsWOUseridSerializer:
    def __init__(self, posts: dict):
        self.posts = posts

    def data(self):
        """
        serialize data
        :return: dict with the fields we need and in the right order
        """
        return {
            "id": self.posts['id'],
            "title": self.posts["title"],
            "body": self.posts["body"]
        }


class PostsSerializer:
    def __init__(self, posts: dict):
        self.posts = posts

    def data(self):
        """
        serialize data
        :return: dict with the fields we need and in the right order
        """
        return {
            "userid": self.posts['userid'],
            "id": self.posts['id'],
            "title": self.posts["title"],
            "body": self.posts["body"]
        }


class UserPostsSerializer:
    def __init__(self, user_dict: dict, posts_list: list):
        self.users = user_dict
        self.posts = posts_list

    def data(self):
        return {
            "id": self.users["id"],
            "username": self.users["username"],
            "email": self.users["email"],
            "first_name": self.users["first_name"],
            "last_name": self.users["last_name"],
            "posts": self.posts
        }


class UserPostsListSerializer:
    def __init__(self, user_list: list, posts_list: list):
        self.users = user_list
        self.posts = posts_list

    @staticmethod
    def serializer_posts_without_userid(post):
        return {
            "id": post['id'],
            "title": post["title"],
            "body": post["body"]
        }

    def data(self):

        result = []
        for user in self.users:
            # Grop posts by userid
            posts = list(filter(lambda post: post['userid'] == user['id'], self.posts))
            serialized_posts = list(map(self.serializer_posts_without_userid, posts))
            result.append(UserPostsSerializer(user, serialized_posts).data())

        return result
