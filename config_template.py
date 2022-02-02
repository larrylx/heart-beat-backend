class DefaultConfig(object):

    # MySQL
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost:3306/login'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

    # JWT
    JWT_SECRET = 'JWT_SIGNATURE'
