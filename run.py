from app import create_app
from models import test_connection

app = create_app()

if __name__ == '__main__':
    # test_connection()
    app.run(debug=True)