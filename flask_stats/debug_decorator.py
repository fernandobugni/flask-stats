from functools import wraps

from flask_stats.debug_context import debug_context


def debug_decorator(func):
    """ Debug decorator to call the function within the debug context """
    # def decorated_func(*args, **kwargs):
    #     with debug_context(func.__name__):
    #         return_value = func(*args, **kwargs)
    #     return return_value
    # return decorated_func

    @wraps(func)
    def decorated_func(*args, **kwargs):

        if func.__name__ is None: return func(*args, **kwargs)

        with debug_context(func.__name__):
            return_value = func(*args, **kwargs)

        return return_value
    return decorated_func

