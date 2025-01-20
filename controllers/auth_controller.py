from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from utils.jwt_util import generate_jwt
from models.user import find_user_by_email, create_user

def signup():
    data = request.get_json()  # Get data from the frontend
    name = data.get('name')  # Retrieve the name
    email = data.get('email')  # Retrieve the email
    password = data.get('password')  # Retrieve the password

    # Check if the email already exists in the database
    if find_user_by_email(email):
        return jsonify({"message": "Email already exists"}), 400

    # Hash the password before saving it
    hashed_password = generate_password_hash(password)

    # Create new user in the database
    create_user(name, email, hashed_password)

    return jsonify({"message": "User registered successfully"}), 201

def login():
    data = request.get_json()
    email = data['email']
    password = data['password']
    
    user = find_user_by_email(email)
    if user and check_password_hash(user['password'], password):
        token = generate_jwt({"id": user['id'], "email": user['email']})
        return jsonify({"token": token}), 200
    
    return jsonify({"message": "Invalid credentials"}), 401
