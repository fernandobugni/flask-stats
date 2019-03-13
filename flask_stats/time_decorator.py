from functools import wraps

from flask_stats.time_context import time_context


def time_decorator(func):
    """ Debug decorator to call the function within the time context """

    @wraps(func)
    def decorated_func(*args, **kwargs):

        import line_profiler
        profile = line_profiler.LineProfiler()

        f = profile(func)
        return_value = f(*args, **kwargs)

        profile.print_stats()

        return return_value
    return decorated_func

