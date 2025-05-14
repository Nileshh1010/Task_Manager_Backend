from flask import Blueprint
from controllers.task_controller import add_task, get_tasks, complete_task, delete_task_by_id

task_routes = Blueprint('tasks', __name__)

# Remove cross_origin() decorators
task_routes.route('/', methods=['POST'])(add_task)
task_routes.route('/', methods=['GET'])(get_tasks)
task_routes.route('/<int:task_id>/complete', methods=['PUT'])(complete_task)
task_routes.route('/<int:task_id>', methods=['DELETE'])(delete_task_by_id)
