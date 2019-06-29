from flask import Flask, jsonify, render_template
from flask_restful import Api
from flask_jwt_extended import JWTManager

from src.blacklist import BLACKLIST
from src.resources.user import UserLogout, UserRegister, UserLogin, User, TokenRefresh
from src.resources.item import Item, ItemList
from src.resources.store import Store, StoreList
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# if flask app get an error, the server will return 500 with the specific error
app.config['PROPAGATE_EXCEPTION'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True  # enable blacklist feature
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh'] # allow blacklisting for access and refresh tokens
app.secret_key = "qwerty"
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/home')
def homepage():
    return render_template('index.html')


jwt = JWTManager(app)  # data:{username: ,password: }


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:  # Instead of hard coding that, better read it from config file
        return {'is_admin': True}
    return {'is_admin': False}


@jwt.token_in_blacklist_loader
def check_of_token_in_blacklist(decrypted_token):
    return decrypted_token['identity'] in BLACKLIST


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description': 'The token has expired.',
        'error': 'token_expired.'
    }), 401


# when the token is not valid:
@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'message': 'signature verification failed.',
        'error': 'invalid_token.'
    }), 401

# when you send no jwt token at all
@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'message': 'signature verification failed.',
        'error': 'invalid_token.'
    }), 401


# revoke a token, makes it invalid
@jwt.revoked_token_loader
def token_is_revoked():
    return jsonify({
        'message': 'signature verification failed.',
        'error': 'invalid_token.'
    }), 401



# adds the Api of the item
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<string:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')

if __name__ == "__main__":
    from src.db import db
    db.init_app(app)
    app.run(port=5000, debug=True)

