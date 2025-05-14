from flask import Blueprint, request, jsonify
from controllers.category_controller import create_category, get_categories

category_routes = Blueprint('categories', __name__)

@category_routes.route('/', methods=['GET'])
def get_all_categories():
    response, status_code = get_categories()
    return jsonify(response), status_code

@category_routes.route('/', methods=['POST'])
def add_category():
    response, status_code = create_category()
    return jsonify(response), status_code
