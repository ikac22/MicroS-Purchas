from flask import Flask, request, Response, jsonify
from flask_jwt_extended import JWTManager
from configuration import Configuration
from shopModels import *
from flask_migrate import Migrate
from sqlalchemy_utils import database_exists, create_database
from utils import error_msg
from utils.auth_utils import require_auth, role_check
import csv
import io

app = Flask(__name__)
app.config.from_object(Configuration)

if not database_exists(Configuration.SQLALCHEMY_DATABASE_URI):
    create_database(Configuration.SQLALCHEMY_DATABASE_URI)

database.init_app(app)
migrate = Migrate(app, database)


jwt = JWTManager(app=app)
@app.route("/update", methods=["POST"])
@role_check("owner")
@require_auth
def add_product():
    if "file" not in request.files:
        return error_msg("Field file missing.")

    content = request.files["file"].stream.read().decode("utf-8")
    csv_reader = csv.reader(io.StringIO(content))
    cat_map = {}
    products = []
    for i, row in enumerate(csv_reader):
        if len(row) != 3:
            return error_msg(f"Incorrect number of values on line {i}.")

        try:
            price = float(row[2])
        except ValueError:
            return error_msg(f"Incorrect price on line {i}.")
        if price <= 0:
            return error_msg(f"Incorrect price on line {i}.")

        n = Product.query.filter(Product.name == row[1]).count()
        if n != 0:
            return error_msg(f"Product {row[1]} already exists.")

        products.append([row[0].split("|"), Product(name=row[1], price=price)])
        for cat_name in row[0].split("|"):
            cat_map[cat_name] = Category(name=cat_name)

    for k, val in cat_map.items():
        cat = Category.query.filter(Category.name == k).first()
        if cat:
            cat_map[k] = cat
        else:
            database.session.add(val)

    for prod in products:
        for cat_name in prod[0]:
            prod[1].categories.append(cat_map[cat_name])

    database.session.add_all(map(lambda x: x[1], products))
    database.session.commit()

    return Response(status=200)




