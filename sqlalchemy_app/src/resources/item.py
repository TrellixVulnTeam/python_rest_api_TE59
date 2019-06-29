from flask_restful import reqparse, Resource
from flask_jwt_extended import fresh_jwt_required, jwt_required, get_jwt_claims, jwt_optional, get_jwt_identity
from src.models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank."
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item must have a store id."
                        )

    @jwt_required
    def get(self, name):
        try:
            item = ItemModel.find_by_name(name) #  returns an ItemModel object
        except:
            return {'message': 'An error ocurred getting the item'}, 500
        if item:
            return item.json()
        return {'message': "item not found."}, 400

    @fresh_jwt_required
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name {} is already exists".format(name)}, 400  # returns HTTP status bad request
        data = Item.parser.parse_args()
        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return {'message': 'An error ocurred inserting the item'}, 500

        return item.json(), 201


    @jwt_required
    def delete(self, name):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'you are not an admin'}
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()
        try:
            item = ItemModel.find_by_name(name)

            if item is None:
                item = ItemModel(name, **data)
            else:
                item.price = data['price']

            item.save_to_db()
        except:
            return {'message': 'An error ocurred updating the item'}, 500
        return item.json()


class ItemList(Resource):
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        # map an items list: list(map(lambda x: x.json(), ItemModel.query.all()
        items = [x.json() for x in ItemModel.query.all()]
        if user_id:
            return {'items': items}, 200
        return {
                   'items': [item['name'] for item in items],
                   'message': 'More data available if you log in.'
               }, 200
