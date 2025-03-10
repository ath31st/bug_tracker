from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity


def same_id_required(param_name: str):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            current_user_id = int(get_jwt_identity())
            route_user_id = kwargs.get(param_name)

            if current_user_id != route_user_id:
                return (
                    jsonify({"error": "You are not allowed to perform this action"}),
                    403,
                )

            return f(*args, **kwargs)

        return wrapper

    return decorator
