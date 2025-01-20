from flask import Blueprint
from controllers.auth_controller import signup, login

auth_routes = Blueprint('auth', __name__)
auth_routes.route('/signup', methods=['POST'])(signup)
auth_routes.route('/login', methods=['POST'])(login)
