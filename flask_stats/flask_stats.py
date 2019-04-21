import gc
import time
import logging

from flask import Flask, Response
from flask.json import jsonify
from flask import request

from werkzeug.datastructures import TypeConversionDict, ImmutableTypeConversionDict

from flask_stats.record_request import RecordRequest
from flask_stats.sqlite_repository import SqliteRepository


class Stats:

    def __init__(self, app: Flask = None):
        self.app = app
        self.__start_time_epoc = time.time()
        self.__sqlite_repository = SqliteRepository()

        def decorate_endpoints():
            endpoints = {str(x): x.endpoint for x in self.app.url_map.iter_rules()}

            from functools import wraps
            def debug(func):
                 '''decorator for debugging passed function'''
                 @wraps(func)
                 def wrapper(*args, **kwargs):

                     stat_param = request.args.get('stat', default='false', type=str)

                     if(stat_param == 'true'):
                         return "stats!"

                     return func(*args, **kwargs)

                 return wrapper

            app.view_functions[endpoints['/']] = debug(app.view_functions[endpoints['/']])

        @app.before_request
        def before_request():
            decorate_endpoints()

            d = TypeConversionDict(request.cookies)
            d['request_time'] = time.time()
            request.cookies = ImmutableTypeConversionDict(d)
            logging.info("before_request %s" % request)

        @app.after_request
        def after_request(response: Response):
            logging.info("after_request %s of %s" % (response, request))

            duration = time.time() - request.cookies['request_time']
            logging.info("request_time %s" % (duration))

            r = RecordRequest(uri=request.path, response_code=response.status_code, duration=duration)
            self.__sqlite_repository.save_request(r)

            return response

        @app.route('/stats')
        def stats():
            return jsonify(self.get_stats())

        @app.route('/endpoints_stats')
        def endpoints_stats():
            return jsonify({'duration': self.__sqlite_repository.get_requests()})

    def __config_info(self):
        config = dict(self.app.config)

        config['SEND_FILE_MAX_AGE_DEFAULT'] = str(config['SEND_FILE_MAX_AGE_DEFAULT'])
        config['PERMANENT_SESSION_LIFETIME'] = str(config['PERMANENT_SESSION_LIFETIME'])
        config['logger'] = str(self.app.logger)
        return config

    def __uptime_info(self):
        now = time.time() - self.__start_time_epoc

        days, hours, minutes, seconds = now // 86400, now // 3600 % 24, now // 60 % 60, now % 60
        uptime_readable = {'days': days, 'hours': hours, 'minutes': minutes, 'seconds': seconds}

        return now, uptime_readable

    @staticmethod
    def __gc_info():
        d = {}

        d['gc.get_stats'] = gc.get_stats()
        d['gc.isenabled'] = gc.isenabled()
        d['gc.get_debug'] = gc.get_debug()
        d['gc.get_threshold'] = gc.get_threshold()

        return d

    def get_stats(self):
        now, uptime_readable = self.__uptime_info()
        config = self.__config_info()
        gc_stats = self.__gc_info()

        return {'uptime': now, 'uptime_readable': uptime_readable, 'config': config, 'gc_stats': gc_stats}
