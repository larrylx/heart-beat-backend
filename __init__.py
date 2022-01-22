from flask import Flask

from common.db import db
from dashboard import dashboard_bp


def create_flask_app(config, env_config_file=None):
    app = Flask(__name__)
    app.config.from_object(config)

    if env_config_file:
        app.config.from_envvar(env_config_file, silent=True)

    # Register Dashboard Blue Print
    app.register_blueprint(dashboard_bp)

    # init database
    db.init_app(app)

    return app
