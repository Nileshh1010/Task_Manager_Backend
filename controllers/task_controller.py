from flask import request, jsonify
from utils.jwt_util import decode_jwt
from models.task import create_task, get_tasks_by_user, mark_task_complete, delete_task
from werkzeug.exceptions import BadRequest

def add_task():
    data = request.get_json()
    user_id = decode_jwt(request.headers.get('Authorization'))['id']
    title = data['title']
    priority = data['priority']
    deadline = data['deadline']

    # Call create_task to insert the task and get the task data back
    task = create_task(title, priority, deadline, user_id)

    return jsonify({"message": "Task added successfully", "task": task}), 201
def get_tasks():
    try:
        # Decode JWT and extract user ID
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"error": "Authorization header is missing"}), 400

        # Assuming `decode_jwt` function is used to decode JWT token and extract user id
        user_id = decode_jwt(auth_header)['id']
        print("Decoded user ID:", user_id)

        # Get tasks for the user
        tasks = get_tasks_by_user(user_id)
        print("Tasks retrieved:", tasks)

        if tasks is None:
            return jsonify({"error": "No tasks found"}), 404

        # If tasks are found, return the tasks in the correct format
        return jsonify({"tasks": tasks}), 200
    
    except Exception as e:
        print("Error in get_tasks:", str(e))
        return jsonify({"error": "Internal server error"}), 500
def complete_task(task_id):
    mark_task_complete(task_id)
    return jsonify({"message": "Task marked as complete"}), 200

def delete_task_by_id(task_id):
    delete_task(task_id)
    return jsonify({"message": "Task deleted successfully"}), 200
