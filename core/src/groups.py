from flask import request, Response, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from core.models.group import Group, GroupSchema

# @api.route('/groups')
# def get_groups():
#     groups = Group.query.all()
#     return jsonify({'data': 'groups123'})


class GroupsApi(Resource):
    @jwt_required
    def get(self):
        all_groups = Group.query.all()
        groups_schema = GroupSchema(many=True)
        result = groups_schema.dump(all_groups)
        return jsonify(result)

