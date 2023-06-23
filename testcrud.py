import json

import crud

# 2
def test_get_all_posts():
    query = crud.get_all_posts()
    result = [i.to_dict() for i in query]
    return result

# 3
def test_get_posts_by_author(user_id):
    query = crud.get_posts_by_author(user_id)
    result = [i.to_dict() for i in query]
    return result

#4
def test_get_post_by_author(post_id):
    query = crud.get_post_by_id(post_id)
    # result = [i.to_dict() for i in query]
    return query.to_dict()

# 4.1
def test_create_post(value):
    pass

# 4.2
def test_update_post(value):
    pass

# 4.3
def test_delete_post(post_id):
    pass


if __name__ == '__main__':

    # print(test_get_all_posts()) # 2
    # print(test_get_posts_by_author(1)) # 3
    print(test_get_post_by_author(1)) # 4