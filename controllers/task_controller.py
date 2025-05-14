from flask import request, jsonify
from utils.jwt_util import decode_jwt
from models.task import (
    create_task,
    get_tasks_by_user,
    update_task_status,
    delete_task,
    get_task_by_id  # Added this function import
)
from models.tracking import create_tracking_entry  # Corrected import
from datetime import datetime


def add_task():
    data = request.get_json()
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"error": "Authorization header missing"}), 401

    decoded = decode_jwt(auth_header)
    if not decoded:
        return jsonify({"error": "Invalid or expired token"}), 401

    user_id = decoded['id']
    title = data['title']
    priority = data['priority']
    deadline = data['deadline']
    category_id = data.get('category_id')

    task = create_task(title, priority, deadline, user_id, category_id)
    return jsonify({"message": "Task added successfully", "task": task}), 201


def get_tasks():
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"error": "Authorization header is missing"}), 400

        user_id = decode_jwt(auth_header)['id']
        tasks = get_tasks_by_user(user_id)

        if tasks is None:
            return jsonify({"error": "No tasks found"}), 404

        return jsonify({"tasks": tasks}), 200
    except Exception as e:
        print("Error in get_tasks:", str(e))
        return jsonify({"error": "Internal server error"}), 500


def complete_task(task_id):
    try:
        task = get_task_by_id(task_id)
        if not task:
            return jsonify({"error": "Task not found"}), 404

        old_status = task['status']
        new_status = "Completed"

        # Add to tracking (updated function call)
        create_tracking_entry(task_id, old_status, new_status)  # Corrected function call

        # Update task status
        update_task_status(task_id, new_status)

        return jsonify({"message": "Task marked as complete"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def delete_task_by_id(task_id):
    delete_task(task_id)
    return jsonify({"message": "Task deleted successfully"}), 200
