from flask import current_app, g
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import load_only

from common.utils.jwt import generate_jwt
from common.utils.decorators import login_required
from common.db import db
from common.db.user_basic import UserBasic
from common.db.click_log import ClickLog
from common.scheduler import scheduler
from common.scheduler.tasks import check_in_alert_user


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
    Post: User Sign up
    Put: Select User Page
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
    Post: Handle User Click
    Put: Display User Dashboard Info
    """
    decorators = [login_required]

    def _seconds_to_dhms(self, seconds):
        days = seconds // (3600 * 24)
        hours = (seconds // 3600) % 24
        minutes = (seconds // 60) % 60
        seconds = round(seconds % 60)
        return days, hours, minutes, seconds

    def post(self):
        user_target = UserBasic.query\
            .options(load_only(UserBasic.id, UserBasic.click_gap))\
            .filter_by(id=g.user_id)\
            .first()

        now = datetime.now(timezone.utc)
        # reminder_time = now + timedelta(hours=user_target.click_gap)
        reminder_time = now + timedelta(seconds=8)

        new_click = ClickLog(user_id=g.user_id, click_time=now)
        db.session.add(new_click)
        db.session.commit()

        reminder = scheduler.add_job(
            func=check_in_alert_user,
            args=g.user_id,
            trigger="date",
            run_date=reminder_time,
            id=f"check_in_alert_{g.user_id}",
            name=f"Alert User {g.user_id} to check-in in {user_target.click_gap} hour(s)",
            replace_existing=True,
        )

        return {'message': {'Check In Succeed': now.strftime("%m/%d/%Y, %H:%M:%S"),
                            'Scheduler Add': reminder.name}}, 201

    def put(self):
        user_target = UserBasic.query.filter_by(id=g.user_id).first()

        last_check_in = ClickLog.query \
            .filter_by(user_id=g.user_id) \
            .order_by(ClickLog.click_time.desc()) \
            .limit(5) \
            .all()

        last_check_list = [record.click_time.strftime("%m/%d/%Y, %H:%M:%S") for record in last_check_in]

        time_diff = datetime.now(timezone.utc).replace(tzinfo=None) - last_check_in[0].click_time

        days, hours, minutes, seconds = self._seconds_to_dhms(time_diff.total_seconds())

        return {'message': {
            'click_gap': user_target.click_gap,
            'user_email': user_target.remind_email,
            'last_five_check_in': last_check_list,
            'Days since Last Check In': days,
            'Hors since Last Check In': hours,
            'Mins since Last Check In': minutes,
            'Secs since Last Check In': seconds,
        }}, 200
