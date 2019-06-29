from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from src.security import authenticate, identity
from src.user import UserRegister
from src.item import Item, ItemList

app = Flask(__name__)
app.secret_key = "qwerty"
api = Api(app)

# configure the endpoint (/auth  on default) to a /login endpoint
app.config['JWT_AUTH_URL_RULE'] = '/login'
# conigure JWT to expire within half an hour
jwt = JWT(app, authenticate, identity)  # data:{username: ,password: }
# configure JTW auth name to be 'email' instead of default 'username'
# app.config['JWT_AUTH_USERNAME_KEY'] = 'email'

# adds the Api of the item
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == "__main__":
    app.run(port=5000, debug=True)

