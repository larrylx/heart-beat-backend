from flask import current_app, g
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from datetime import datetime, timezone

from common.utils.jwt import generate_jwt
from common.utils.decorators import login_required
from common.db import db
from common.db.user_basic import UserBasic
from common.db.click_log import ClickLog


class Authorization(Resource):
    """
    User Log In
    """
    def _generate_tokens(self, user_id):
        """
        Generate token
        :param user_id: string
        :return: token
        """
        token = generate_jwt({'user_id': user_id})
        return token

    def get(self):
        return {'message': 'I\'m a teapot'}, 418

    def post(self):
        user_info_parser = RequestParser()
        user_info_parser.add_argument('user_id', required=True, location='json')
        args = user_info_parser.parse_args()
        user_id = args.user_id

        user_target = UserBasic.query.filter_by(id=user_id).first()

        if user_target is None:
            return {'message': 'User Not Found'}, 400
        else:
            token = self._generate_tokens(user_id)
            return {'message': {'token': token}}, 200


class Dashboard(Resource):
    """
    Select User Page/User Sign up Page
    """
    def post(self):
        """
        User Sign Up
        :return:
        """
        pass

    def put(self):
        """
        Display List of Users
        :return: List of Users
        """
        user_top6 = UserBasic.query.limit(6).all()

        user_list = []

        for user in user_top6:
            user_list.append({
                "user_name": user.name,
                "user_id": user.id,
                "user_photo": user.picture
            })

        return {'message': user_list}, 200


class UserDashboard(Resource):
    """
    Handle User Click
    """
    decorators = [login_required]

    def post(self):
        now = datetime.now(timezone.utc)
        new_click = ClickLog(user_id=g.user_id, click_time=now)
        db.session.add(new_click)
        db.session.commit()
        return {'message': {'Check In Succeed': now.strftime("%m/%d/%Y, %H:%M:%S")}}, 201

    def put(self):
        user_target = UserBasic.query.filter_by(id=g.user_id).first()
        last_check_in = ClickLog.query\
            .filter_by(user_id=g.user_id)\
            .order_by(ClickLog.click_time.desc())\
            .limit(5)\
            .all()

        last_check_list = [record.click_time.strftime("%m/%d/%Y, %H:%M:%S") for record in last_check_in]

        if user_target is None:
            return {'message': 'Unauthorized'}, 401

        else:
            return {'message': {
                'click_gap': user_target.click_gap,
                'user_email': user_target.remind_email,
                'last_five_check_in': last_check_list
            }}, 200
