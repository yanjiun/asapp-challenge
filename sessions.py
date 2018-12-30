import contextlib

# this class managers tokens & login sessions

def login_user(conn, user_id):
    # TODO: generate random string token
    token = "jjdjkfjdksj"
    return token

def update_user_token(conn, user_id, token):
    # TODO: update db
    # update the db

def authenticate(conn, user_id, token):
    # TODO: checks db to authenticate user tokens
    # return False if not authenticated
    return True
