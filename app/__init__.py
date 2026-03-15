import os
from flask import Flask, jsonify, request, redirect, url_for
from flask_login import LoginManager
from .models import db, User
from dotenv import load_dotenv

login_manager = LoginManager()

def create_app():
    load_dotenv()
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev-secret'),
        SQLALCHEMY_DATABASE_URI='sqlite:///chat.db',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        # Enable dev auth bypass when set to '1' in environment (dev use only)
        DEV_AUTH_BYPASS=(os.environ.get('DEV_AUTH_BYPASS', '0') == '1')
    )

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    with app.app_context():
        db.create_all()

    # Register blueprints
    from .views import main_bp
    app.register_blueprint(main_bp)

    return app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized_handler():
    # Return JSON for API routes, redirect for web pages
    if request.path.startswith('/api/'):
        return jsonify({'error': 'unauthorized'}), 401
    return redirect(url_for('main.login'))
