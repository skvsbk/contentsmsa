def serializer_posts_without_userid(response):
    """
    serialize data
    :param response: dict with all fields from DB
    :return: dict with the fields we need and in the right order
    """
    return {
        "id": response['id'],
        "title": response["title"],
        "body": response["body"]
    }


def serializer_posts(response):
    """
    serialize data
    :param response: dict with all fields from DB
    :return: dict with the fields we need and in the right order
    """
    return {
        "userid": response['userid'],
        "id": response['id'],
        "title": response["title"],
        "body": response["body"]
    }
