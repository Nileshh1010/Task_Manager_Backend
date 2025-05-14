from flask import Flask, request, jsonify
from flask_cors import CORS
from db.database import init_db
from routes.auth_routes import auth_routes
from routes.task_routes import task_routes
from routes.category_routes import category_routes
from routes.notification_routes import notification_routes
from routes.tracking_routes import tracking_routes
import os

app = Flask(__name__)
CORS(app, 
     origins=["http://localhost:8080"],
     allow_credentials=True,
     supports_credentials=True,
     expose_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization"])

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')

@app.after_request
def after_request(response):
    origin = request.headers.get('Origin')
    if origin == 'http://localhost:8080':
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

@app.before_request
def handle_options_request():
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        origin = request.headers.get('Origin')
        if origin == 'http://localhost:8080':
            response.headers['Access-Control-Allow-Origin'] = origin
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response, 200

# Initialize Database
init_db()

# Register Blueprints
app.register_blueprint(auth_routes, url_prefix='/auth')
app.register_blueprint(task_routes, url_prefix='/tasks')
app.register_blueprint(category_routes, url_prefix='/categories')
app.register_blueprint(notification_routes, url_prefix='/notifications')
app.register_blueprint(tracking_routes, url_prefix='/tracking')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)  # Ensure the server listens on port 8000
