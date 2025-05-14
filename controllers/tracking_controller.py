from flask import jsonify, request
from models.tracking import get_task_history, create_tracking_entry
from models.task import get_tasks_by_user, update_task_status

def get_task_tracking(task_id):
    try:
        history = get_task_history(task_id)
        return jsonify({
            "history": [{
                "changed_at": entry["changed_at"],
                "from": entry["from"],
                "to": entry["to"],
                "task_id": entry["task_id"],
                "title": entry["title"]
            } for entry in history]
        }), 200
    except Exception as e:
        print(f"Error getting tracking history: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

def track_status_change(task_id):
    try:
        task = get_tasks_by_user(task_id)
        if not task:
            return jsonify({"error": "Task not found"}), 404

        current_status = task["status"]
        new_status = request.json.get("status")
        
        if not new_status:
            return jsonify({"error": "New status is required"}), 400

        if create_tracking_entry(task_id, current_status, new_status):
            if update_task_status(task_id, new_status):
                return jsonify({"message": "Status updated successfully"}), 200
            
        return jsonify({"error": "Failed to update status"}), 500
    except Exception as e:
        print(f"Error tracking status change: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500
