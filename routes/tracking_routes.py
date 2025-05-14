from flask import Blueprint, request
from controllers.tracking_controller import get_task_tracking, track_status_change
from flask_cors import cross_origin

tracking_routes = Blueprint('tracking', __name__)

# Route to get task tracking history
tracking_routes.route('/<int:task_id>', methods=['GET'])(cross_origin()(get_task_tracking))

# Route to update task status
tracking_routes.route('/<int:task_id>/status', methods=['POST'])(cross_origin()(track_status_change))

# Allow CORS for specific frontend origin
@tracking_routes.after_request
def add_cors_headers(response):
    origin = request.headers.get('Origin')
    if origin == 'http://localhost:8080':
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response
