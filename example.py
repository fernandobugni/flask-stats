
from time import sleep

from flask import Flask

from flask_stats.time_decorator import time_decorator
from flask_stats.flask_stats import Stats

app = Flask(__name__)
Stats(app)

@app.route('/')
@time_decorator
def hello():
    a = 40
    sleep(10)
    b = a + 50
    return 'Hello, World %s !' % b


if __name__ == '__main__':
    app.run()

    # In order to run a function that is subscripted by a route
    # you have to do: app.view_functions['hello']()

    # To search for the endpoint method could be
    # [x for x in app.url_map.iter_rules()]

    # To add code by metaprogramming
    # from functools import wraps
    # def debug(func):
    #     '''decorator for debugging passed function'''
    #     @wraps(func)
    #     def wrapper(*args, **kwargs):
    #         print("Full name of this method:", func.__qualname__)
    #         return func(*args, **kwargs)
    #     return wrapper
    # def f():
    #     print("111")
    #
    # debug(f)
    # <function f at 0x7f5e1db86510>
    # debug(f)()
    # Full name of this method: f
    # 111