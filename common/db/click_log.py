from . import db


class ClickLog(db.Model):
    """
    Every User Check-In Record
    """
    __tablename__ = 'click_log'

    class STATUS:
        ENABLE = 1
        DISABLE = 0

    id = db.Column('click_id', db.Integer, primary_key=True, doc='Click ID')
    user_id = db.Column(db.Integer, nullable=False, doc='Click ID')
    click_time = db.Column(db.DateTime, nullable=False, doc='User Check-In Time')
