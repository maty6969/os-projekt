from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.models import db
import os

def create_app():
    app = Flask(__name__)
    
    # Configuration
    # Pro lokální vývoj používáme SQLite, pro produkci SQL Server
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL',
        'sqlite:///guestbook.db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Initialize database
    db.init_app(app)
    
    # Register blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app
