from flask_restful import reqparse, Resource
from flask_jwt import jwt_required
import sqlite3

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank."
                        )

    @jwt_required()
    def get(self, name):
        try:
            item = self.find_by_name(name)
        except:
            return {'message': 'An error ocurred getting the item'}, 500
        if item:
            return item
        return {'message': "item not found."}, 400

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        # select item query
        query = "SELECT * FROM items WHERE name=?"

        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}


    def post(self, name):
        if self.find_by_name(name):
            return {'message': "An item with name {} is already exists".format(name)}, 400  # returns HTTP status bad request
        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}

        try:
            self.insert(item)
        except:
            return {'message': 'An error ocurred inserting the item'}, 500

        return item, 201

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        # insert query
        query = "INSERT INTO items VALUES(?, ?)"
        cursor.execute(query, (item['name'], item['price']))
        connection.commit()
        connection.close()

    def delete(self, name):
        if self.find_by_name(name) is None:
            return {'message': "An item with name {} is not exists".format(
                name)}, 400  # returns HTTP status bad request

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        # delete query
        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()

        return {'message': 'Item deleted.'}

    def put(self, name):
        data = Item.parser.parse_args()
        try:
            item = self.find_by_name(name)
            updated_item = {'name': name, 'price': data['price']}

            if item is None:
                self.insert(updated_item)
            else:
                self.update(updated_item)
        except:
            return {'message': 'An error ocurred updating the item'}, 500
        return updated_item

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        # update query
        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))
        connection.commit()
        connection.close()


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        # select item query
        query = "SELECT * FROM items"

        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({
                'name': row[0],
                'price': row[1]
            })

        connection.commit()
        connection.close()

        return {'items': items}
