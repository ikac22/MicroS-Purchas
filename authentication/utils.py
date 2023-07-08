from flask import jsonify


def error_msg(msg, status=400):
    res = jsonify({"message": msg})
    res.status = status
    return res

