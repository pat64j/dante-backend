from flask import request, Response, jsonify
from flask_restful import Resource


class HomeApi(Resource):
    def get(self):
        ret = {"message":"Home route success", "data": "This is an endpoint to test this api"}
        return ret, 200

