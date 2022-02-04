from common.scheduler import scheduler
from common.db.user_basic import UserBasic


def check_in_alert_user(user_id):
    app = scheduler.app
    with app.app_context():
        user_target = UserBasic.query.filter_by(id=user_id).first()
        print(user_target.remind_email)
