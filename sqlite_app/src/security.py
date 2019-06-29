from werkzeug.security import safe_str_cmp
from src.user import User


# This is authenticate in the user login and gives a JWT token to the user
def authenticate(username, password):
    user = User.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user


# payload is the JWT token
def identity(payload):
    user_id = payload['identity']
    return User.find_by_id(user_id)

