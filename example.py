
from time import sleep
from flask import Flask
from flask_stats import Stats

s = Stats()

app = Flask(__name__)
s.init_app(app)


@app.route('/')
def hello():
    a = 40
    sleep(10)
    b = a + 50
    return 'Hello, World %s !' % b


if __name__ == '__main__':
    app.run()
