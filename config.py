# config.py
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
    MAIL_USERNAME = 'example@gmail.com'  # ← CHANGE THIS
    MAIL_PASSWORD = 'your_key_here'    # ← App Password (NOT regular password!)
    MAIL_DEFAULT_SENDER = 'example@gmail.com'