from flask import Flask

from common.db import db
from dashboard import dashboard_bp
from common.utils.middlewares import token_validation
from common.utils.snowflake import IdWorker
from common.scheduler import scheduler


def create_flask_app(config, env_config_file=None):
    app = Flask(__name__)
    app.config.from_object(config)

    if env_config_file:
        app.config.from_envvar(env_config_file, silent=True)

    # Register Hook
    app.before_request(token_validation)

    # Register APScheduler
    scheduler.init_app(app)
    scheduler.start()

    # Register Dashboard Blue Print
    app.register_blueprint(dashboard_bp)

    # init database
    db.init_app(app)

    # Register Snowflake to app
    app.snowflake = IdWorker(app.config['DATACENTER_ID'],
                             app.config['WORKER_ID'],
                             app.config['SEQUENCE'])

    return app
