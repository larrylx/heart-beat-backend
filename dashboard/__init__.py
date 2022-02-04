from flask import Blueprint
from flask_restful import Api

from . import dashboard
from common.utils.output_json import output_json

dashboard_bp = Blueprint('Dashboard', __name__, url_prefix='/dashboard')
dashboard_api = Api(dashboard_bp, catch_all_404s=True)
dashboard_api.representation('application/json')(output_json)

dashboard_api.add_resource(dashboard.MainDashboard, '/', endpoint='User_List')

dashboard_api.add_resource(dashboard.SignUp, '/signup', endpoint='User_Sign_Up')

dashboard_api.add_resource(dashboard.Authorization, '/login', endpoint='User_Log_In')

dashboard_api.add_resource(dashboard.UserDashboard, '/user', endpoint='User_Dashboard')
