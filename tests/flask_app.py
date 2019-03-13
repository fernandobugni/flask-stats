from flask import Flask
from time import sleep
from flask_stats.flask_stats import Stats


def create_app():

    app = Flask(__name__)
    Stats(app)

    @app.route('/')
    def hello():
        sleep(10)
        return 'Hello, World!'

    return app
