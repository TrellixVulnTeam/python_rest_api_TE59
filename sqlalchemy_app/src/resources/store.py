from flask_restful import Resource
from src.models.store import StoreModel

class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 200
        return {'message': 'store not found.'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': 'The store with name {} already exists.'.format(name)}, 404
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': 'An error ocurred creating the store.'}, 500
        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {'message': 'Store deleted.'}


class StoreList(Resource):
    def get(self):
        return {'stores': [x.json() for x in StoreModel.find_all()]}

