from flask import Flask
from views import app_views

app = Flask(__name__)


app.register_blueprint(app_views)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)