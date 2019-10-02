"""
Utility helpers as decorator
"""
import functools
import logging
from flask import request
from flask_restplus import abort

from api.schema.offset_limit import OffsetLimitSchema
from api.schema.set_up_schema_params import set_up_schema
from app.core.manager.token import validate_token

LOGGER = logging.getLogger('main')


def memoize(func):
    """
    Memoize function, can be used as decorator
    Does not share memoized cache between processes
    :param func: function should be cache
    :return:
    """
    memoized_cache = dict()

    def memoized_func(*args):
        if args in memoized_cache:
            return memoized_cache[args]
        result = func(*args)
        memoized_cache[args] = result
        return result

    return memoized_func


def method_dispatch(func):
    dispatcher = functools.singledispatch(func)

    def wrapper(*args, **kw):
        return dispatcher.dispatch(args[1].__class__)(*args, **kw)

    wrapper.register = dispatcher.register
    functools.update_wrapper(wrapper, func)
    return wrapper


def ignore_first_call(fn):
    called = False

    def wrapper(*args, **kwargs):
        nonlocal called
        if called:
            return fn(*args, **kwargs)
        else:
            called = True
            return None

    return wrapper


def authorized(fn):
    """Decorator that checks that requests
    contain an id-token in the request header.

    Usage:
    @app.route("/")
    @authorized
    """
    def _wrap(*args, **kwargs):
        pass

        return fn(*args, **kwargs)

    return _wrap


def validate_offset_limit(fn):
    """Decorator that validate offset limit in request.args
       Usage:
       @validate_offset_litmit
       """

    def _wrap(*args, **kwargs):
        params = request.args
        schema_offset_limit = OffsetLimitSchema()
        schema_offset_limit.load_data(params)
        if not (schema_offset_limit.is_valid()):
            abort(400, data={},
                  error={"code": 8,
                         "detail": "Bad request"})
        data = schema_offset_limit.data
        kwargs.update({'limit': data['limit'], 'offset': data['offset']})
        return fn(*args, **kwargs)

    return _wrap


def validate_params(model):
    """Decorator that validate params filter in request.args
       Usage:
       @validate_params(model)
       """

    def decorator(f):
        def _wrap(*args, **kwargs):
            params = request.args
            schema = set_up_schema(model)
            schema.load_data(params)
            if not (schema.is_valid()):
                abort(400, data={},
                      error={"code": 8,
                             "detail": "Bad request"})
            data = schema.data
            kwargs.update(data)
            return f(*args, **kwargs)

        return _wrap

    return decorator
