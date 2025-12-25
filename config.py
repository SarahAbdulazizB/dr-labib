# config.py
import os

class Config:
    SECRET_KEY = 'secretkey-123456'  # Strong rakhna
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'          # XAMPP default
    MYSQL_PASSWORD = ''          # XAMPP default empty
    MYSQL_DB = 'dr_labib'
    MYSQL_CURSORCLASS = 'DictCursor'  # Results dict mein ayein, easy

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'dr.labib2025@gmail.com'  # ← CHANGE THIS
    MAIL_PASSWORD = 'bruc tixi rhrm lvru'    # ← App Password (NOT regular password!)
    MAIL_DEFAULT_SENDER = 'dr.labib2025@gmail.com'

    # ML Model Paths
    MODEL_PATH = os.path.join('app', 'models', 'lstm_model_best.h5')
    LABEL_ENCODER_PATH = os.path.join('app', 'models', 'label_encoder.pkl')