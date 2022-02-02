from flask import current_app
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from common.utils.jwt import generate_jwt
from common.db.user_basic import UserBasic


class UserDashboard(Resource):

    def _generate_tokens(self, user_id):
        """
        Generate token
        :param user_id: string
        :return: token
        """
        token = generate_jwt({'user_id': user_id})
        return token

    def get(self):
        return {'message': 'Get Success'}, 200

    def post(self):
        user_info_parser = RequestParser()
        user_info_parser.add_argument('user_id', required=True, location='json')
        args = user_info_parser.parse_args()
        user_id = args.user_id

        user_target = UserBasic.query.filter_by(id=user_id).first()

        token = self._generate_tokens(user_id)

        if user_target is None:
            return {'message': 'User Not Found'}, 200
        else:
            return {'message': {'click_gap': user_target.click_gap,
                                'user_email': user_target.remind_email,
                                'token': token}}, 200

    def put(self):
        pass


class Dashboard(Resource):

    def post(self):
        user_top6 = UserBasic.query.limit(6).all()

        user_list = []

        for user in user_top6:
            user_list.append({
                "user_name": user.name,
                "user_id": user.id,
                "user_photo": user.picture
            })

        return {'message': user_list}, 200

