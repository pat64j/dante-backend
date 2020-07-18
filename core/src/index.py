from flask import request, Response, jsonify
from flask_restful import Resource


class HomeApi(Resource):
    def get(self):
        ret = {"message":"API test success update 1", "data": "This is an endpoint to test this api"}
        return ret, 200

