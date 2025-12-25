# app/__init__.py
from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from app.user import User
import os

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'danger'

mail = Mail()

def load_ml_models(app):
    """Load LSTM model and label encoder at app startup"""
    try:
        import tensorflow as tf
        import pickle
        
        model_path = app.config['MODEL_PATH']
        encoder_path = app.config['LABEL_ENCODER_PATH']
        
        # Check if files exist
        if not os.path.exists(model_path):
            print(f"WARNING: Model file not found at {model_path}")
            app.config['LSTM_MODEL'] = None
            return False
        
        if not os.path.exists(encoder_path):
            print(f"WARNING: Label encoder not found at {encoder_path}")
            app.config['LABEL_ENCODER'] = None
            return False
        
        # Load LSTM model
        print(f"Loading LSTM model from {model_path}...")
        lstm_model = tf.keras.models.load_model(model_path)
        app.config['LSTM_MODEL'] = lstm_model
        print("LSTM model loaded successfully")
        
        # Load label encoder
        print(f"Loading label encoder from {encoder_path}...")
        with open(encoder_path, 'rb') as f:
            label_encoder = pickle.load(f)
        app.config['LABEL_ENCODER'] = label_encoder
        print("Label encoder loaded successfully")
        
        return True
        
    except Exception as e:
        print(f"Error loading ML models: {str(e)}")
        app.config['LSTM_MODEL'] = None
        app.config['LABEL_ENCODER'] = None
        return False

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialize extensions
    login_manager.init_app(app)
    mail.init_app(app)

    # Load ML models at startup
    load_ml_models(app)

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