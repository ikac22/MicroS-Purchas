from flask import Flask, request, Response, jsonify
from config.authConfig import Configuration
from authModels import *
from sqlalchemy import and_
from flask_migrate import Migrate
from sqlalchemy_utils import database_exists, create_database
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import re
from utils import error_msg
from utils.auth_utils import require_auth

app = Flask(__name__)
app.config.from_object(Configuration)

database.init_app(app)


@app.route("/register_<role>", methods=["POST"])
def register(role):
    if not role or role not in ("courier", "customer"):
        return Response("Not Found", status=404)

    nd = {
        "forename": request.json.get("forename", ""),
        "surname": request.json.get("surname", ""),
        "email": request.json.get("email", ""),
        "password": request.json.get("password", ""),
    }

    for d in nd.items():
        if d[1] == "":
            return error_msg(f"Field {d[0]} is missing.")

    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if not re.fullmatch(regex, nd["email"]):
        return error_msg("Invalid email.")

    if len(nd["password"]) < 8:
        return error_msg("Invalid password.")

    if User.query.filter(User.email == nd["email"]).count():
        return error_msg("Email already exists.")

    user = User(email=nd["email"], password=nd["password"], surname=nd["surname"], forename=nd["forename"], role=role)

    database.session.add(user)
    database.session.commit()

    return Response(status=200)


jwt = JWTManager(app=app)


@app.route("/login", methods=["POST"])
def login():
    nd = {
        "email": request.json.get("email", ""),
        "password": request.json.get("password", ""),
    }

    for d in nd.items():
        if d[1] == "":
            return error_msg(f"Field {d[0]} is missing.")

    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if not re.fullmatch(regex, nd["email"]):
        return error_msg("Invalid email.")

    user = User.query.filter(and_(User.email == nd["email"], User.password == nd["password"])).first()
    if not user:
        return error_msg("Invalid credentials.")

    additional_claims = {
        "surname": user.surname,
        "forename": user.forename,
        "roles": [user.role]
    }

    access_token = create_access_token(identity=user.email, additional_claims=additional_claims)
    return jsonify({"accessToken": access_token})


@app.route("/delete", methods=["POST"])
@jwt_required()
@require_auth
def delete():
    email = get_jwt_identity()
    users = User.query.filter(User.email == email)
    if not users.first():
        return error_msg("Unknown user.")

    users.delete()
    database.session.commit()
    return Response(status=200)
