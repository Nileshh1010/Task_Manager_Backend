from flask import Blueprint
from controllers.task_controller import add_task, get_tasks, complete_task, delete_task_by_id
from flask_cors import cross_origin

task_routes = Blueprint('tasks', __name__)

# Enable CORS for all task routes
task_routes.route('/', methods=['POST'])(cross_origin()(add_task))
task_routes.route('/', methods=['GET'])(cross_origin()(get_tasks))
task_routes.route('/<int:task_id>/complete', methods=['PUT'])(cross_origin()(complete_task))
task_routes.route('/<int:task_id>', methods=['DELETE'])(cross_origin()(delete_task_by_id))
