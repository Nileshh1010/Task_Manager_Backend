from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)  # Bind the app with SQLAlchemy
    with app.app_context():
        db.create_all()  # Create all tables
