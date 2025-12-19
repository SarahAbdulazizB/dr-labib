# app/__init__.py
from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from app.user import User

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'danger'

mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialize extensions
    login_manager.init_app(app)
    mail.init_app(app)

    # Import middleware (for decorators)
    from app import middleware  # noqa

    # Import routes
    from app.routes import auth, dashboard
    
    app.register_blueprint(auth)
    app.register_blueprint(dashboard, url_prefix='/dashboard')

    return app

@login_manager.user_loader
def load_user(user_id):
    from models import get_db_connection
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, full_name, email, role FROM users WHERE id = %s", (user_id,))
        user_data = cursor.fetchone()
        cursor.close()
        conn.close()
        if user_data:
            return User(
                id=user_data[0],
                full_name=user_data[1],
                email=user_data[2],
                role=user_data[3]
            )
    return None