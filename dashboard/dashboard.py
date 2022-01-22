from flask import current_app
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from common.db.user_basic import UserBasic


class UserDashboard(Resource):

    def get(self):
        return {'message': 'Get Success'}, 200

    def post(self):
        user_info_parser = RequestParser()
        user_info_parser.add_argument('user_name', required=True, location='json')
        user_info_parser.add_argument('user_id', required=True, location='json')
        args = user_info_parser.parse_args()
        # user_name = args.user_name
        user_id = args.user_id

        user_target = UserBasic.query.filter_by(id=user_id).first()

        if user_target is None:
            return {'message': 'User Not Found'}, 200
        else:
            return {'message': {'click_time': user_target.click_time, 'user_picture': user_target.picture}}, 200
