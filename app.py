from flask import Flask
from db.database import init_db
from routes.auth_routes import auth_routes
from routes.task_routes import task_routes
from flask_cors import CORS
app = Flask(__name__)
cors = CORS(app, resources={
    r"/*": {
        "origins": ["https://task-manager-frontend-eight-teal.vercel.app"],  # Frontend URL
        # Allow sending cookies
        "supports_credentials": True 
        }
})



import os
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')

# Initialize Database
init_db()

# Register Blueprints
app.register_blueprint(auth_routes, url_prefix='/auth')
app.register_blueprint(task_routes, url_prefix='/tasks')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000)
