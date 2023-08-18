from flask import jsonify


def error_msg(msg, status=400):
    if msg == "Missing Authorization Header":
        res = jsonify({"msg":msg})
    else:
        res = jsonify({"message": msg})
    res.status = status
    return res

def read_file ( path ):
    with open ( path, "r" ) as file:
        return file.read ( )
