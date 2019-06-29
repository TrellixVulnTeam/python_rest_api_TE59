from werkzeug.security import safe_str_cmp
from flask_jwt_extended import get_raw_jwt, jwt_required, get_jwt_identity, jwt_refresh_token_required, create_access_token, create_refresh_token
from flask_restful import Resource, reqparse
from src.models.user import UserModel
from src.blacklist import BLACKLIST


_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                          type=str,
                          required=True,
                          help="This field cannot be left blank")
_user_parser.add_argument('password',
                          type=str,
                          required=True,
                          help="This field cannot be left blank")


class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {'message': 'username is already exists'}, 400
        
        user = UserModel(**data)
        user.save_to_db()

        return {'message': 'User created successully.'}, 201


class User(Resource):
    @jwt_required
    def get(self, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'uUser not found.'}, 404
        user.delete_from_db()
        return {'message': 'User deleted.'}


class UserLogin(Resource):
    @classmethod
    def post(cls):
        data = _user_parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        # this is what 'authenticate used to do
        if user and safe_str_cmp(user.password, data['password']):
            # identity = what the 'identity' function used to do
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        return {'message': 'Invalid credentials.'}, 401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']  # jti is a uniquie identifer for jwt
        BLACKLIST.add(jti)
        return {'message': 'Successfully logged out.'}, 200



class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'acess_token': new_token}, 200
