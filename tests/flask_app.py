from flask import Flask
from time import sleep
from flask_stats import Stats


def create_app():

    s = Stats()
    app = Flask(__name__)
    s.init_app(app)

    @app.route('/')
    def hello():
        sleep(10)
        return 'Hello, World!'

    return app
