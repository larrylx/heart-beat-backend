from . import db


class UserBasic(db.Model):
    """
    User basic information From
    """
    __tablename__ = 'user_basic'

    class STATUS:
        ENABLE = 1
        DISABLE = 0

    id = db.Column('user_id', db.Integer, primary_key=True, doc='User ID')
    name = db.Column('user_name', db.String, nullable=False, doc='User Name')
    status = db.Column(db.Integer, default=1, nullable=False, doc='User Status, 0-Disable，1-Normal')
    click_time = db.Column(db.Integer, primary_key=True, doc='Hours Need to Re click')
    remind_email = db.Column(db.String, unique=True, nullable=False, doc='Reminder Email')
    alert_email = db.Column(db.String, unique=True, nullable=False, doc='Alert Email')
    picture = db.Column('profile_photo', db.String, doc='Profile Picture')
    last_login = db.Column(db.DateTime, doc='User Last Log in Time')
