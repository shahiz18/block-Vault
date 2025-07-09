import os
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
load_dotenv()  

db = SQLAlchemy()

def create_app():
    template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
    app = Flask(__name__, template_folder=template_dir)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vaultlog_test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), '..', 'uploads')
    
    app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET", "dev‑fallback")
    app.config['PINATA_JWT'] = os.environ.get("PINATA_JWT")
    db.init_app(app)

    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # Redirects to 'auth.login' if not logged in
    login_manager.init_app(app)

    from .models import User
    

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    from .routes import main
    app.register_blueprint(main)

    from .auth import auth
    app.register_blueprint(auth)

    with app.app_context():
        db.create_all()

    return app
