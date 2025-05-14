from flask import Blueprint
from controllers.notification_controller import create_notification, get_notifications
from flask_cors import cross_origin

notification_routes = Blueprint('notifications', __name__)

# Route to create a new notification (POST request)
notification_routes.route('/', methods=['POST'])(cross_origin()(create_notification))

# Route to get all notifications for the user (GET request)
notification_routes.route('/', methods=['GET'])(cross_origin()(get_notifications))
