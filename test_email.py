# test_email.py
from flask import Flask
from flask_mail import Mail, Message
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
mail = Mail(app)

with app.app_context():
    try:
        msg = Message(
            subject='Test Email - Dr-labib',
            recipients=['example@gmail.com']  # ← Send to yourself
        )
        msg.body = "If you receive this, email setup is working! 🎉"
        mail.send(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")