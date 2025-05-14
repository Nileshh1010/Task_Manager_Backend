from flask import request, jsonify
from models.category import add_category, get_all_categories
from utils.jwt_util import decode_jwt
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_category():
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return {"error": "Authorization header missing"}, 401
            
        token = auth_header.replace('Bearer ', '')
        user_data = decode_jwt(token)
        if not user_data or 'id' not in user_data:
            return {"error": "Invalid authentication"}, 401

        data = request.get_json()
        if not data or 'name' not in data:
            return {"error": "Category name is required"}, 400

        category = add_category(name=data['name'], user_id=user_data['id'])
        logger.info(f"Category created successfully: {category}")
        return {"category": category}, 201

    except Exception as e:
        logger.error(f"Error creating category: {str(e)}")
        return {"error": "Internal server error"}, 500

def get_categories():
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return {"error": "Authorization header missing"}, 401
            
        token = auth_header.replace('Bearer ', '')
        user_data = decode_jwt(token)
        if not user_data or 'id' not in user_data:
            return {"error": "Invalid authentication"}, 401

        categories = get_all_categories(user_id=user_data['id'])
        logger.info(f"Retrieved {len(categories)} categories")
        return {"categories": categories}, 200

    except Exception as e:
        logger.error(f"Error fetching categories: {str(e)}")
        return {"error": "Internal server error"}, 500
