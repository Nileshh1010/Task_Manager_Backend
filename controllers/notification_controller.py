from flask import request, jsonify
from utils.jwt_util import decode_jwt
from models.notification import save_notification_to_db, get_notifications_by_user

# Create a new notification
def create_notification():
    data = request.get_json()  # Get JSON data from the request
    user_id = decode_jwt(request.headers.get('Authorization'))['id']  # Decode JWT to get user ID
    message = data.get('message')  # Get message from the request data
    timestamp = data.get('timestamp')  # Get timestamp (ISO datetime)

    # Check if message and timestamp are provided
    if not message or not timestamp:
        return jsonify({"error": "Message and timestamp are required"}), 400

    # Save the notification to the database
    notification = save_notification_to_db(user_id, message, timestamp)
    
    # Return the created notification
    return jsonify({"message": "Notification created", "notification": notification}), 201

# Get all notifications for a specific user
def get_notifications():
    user_id = decode_jwt(request.headers.get('Authorization'))['id']  # Decode JWT to get user ID
    notifications = get_notifications_by_user(user_id)  # Fetch notifications for the user
    return jsonify({"notifications": notifications}), 200
