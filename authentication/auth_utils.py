from functools import wraps
from utils import error_msg
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask import request


def require_auth(function):
    def decorator(*arguments, **kwarguments):
        if "Authorization" not in request.headers:
            return error_msg("Missing Authorization Header", status=401)
        return function(*arguments, **kwarguments)

    return decorator


def role_check(role):
    def inner_role_check(function):
        @wraps(function)
        def decorator(*arguments, **kwarguments):
            verify_jwt_in_request()

            claims = get_jwt()
            if "role" not in claims and claims["role"] == role:
                return function(*arguments, **kwarguments)
            else:
                return error_msg("Permission denied.", status=403)

        return decorator

    return inner_role_check
