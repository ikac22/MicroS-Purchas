import datetime

from flask import Flask, request, Response, jsonify
from flask_jwt_extended import JWTManager, get_jwt_identity
from sqlalchemy import and_
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


@app.route("/search", methods=["GET"])
@role_check("buyer")
@require_auth
def search_products():
    name = request.args.get("name", "")
    category = request.args.get("category", "")

    products = database.session.query(Product).join(Product.categories) \
        .filter(
        and_(Category.name.like(f"%{category}%"),
             Product.name.like(f"%{name}%"))
    ).distinct()

    categories = database.session.query(Category).join(Category.products) \
        .filter(
        and_(Category.name.like(f"%{category}%"),
             Product.name.like(f"%{name}%"))
    ).distinct()

    res_cats = [cat.name for cat in categories]
    res_prods = [
        {"categories": [cat.name for cat in prod.categories], "id": prod.id, "name": prod.name, "price": prod.price}
        for prod in products
    ]

    return jsonify(categories=res_cats, products=res_prods)


@app.route("/order", methods=["POST"])
@role_check("buyer")
@require_auth
def order_product():
    reqs = request.json.get("requests")
    if not reqs:
        return error_msg("Field requests is missing.")

    o = OrderStat(bemail=get_jwt_identity(), status="CREATED", created=datetime.datetime.now())
    fields = {"id": 0, "quantity": 0}
    price = 0
    pos = []
    for i, p in enumerate(reqs):
        for f in fields:
            if f not in p:
                return error_msg(f"Product {f} is missing for request number {i}.")

        for f in fields:
            try:
                fields[f] = int(p[f])
            except ValueError:
                return error_msg(f"Invalid product {f} for request number {i}.")
            if fields[f] <= 0:
                return error_msg(f"Invalid product {f} for request number {i}.")

        product = Product.query.filter(Product.id == fields["id"]).first()
        if not product:
            return error_msg(f"Invalid product for request number {i}.")
        pos.append(ProductOrder(order=o, quantity=fields["quantity"], product=product))
        price += product.price*fields["quantity"]

    o.price = price
    database.session.add(o)
    database.session.add_all(pos)
    database.session.commit()

    return Response(status=200)


@app.route("/status", methods=["GET"])
@role_check("buyer")
@require_auth
def order_status():
    orders = OrderStat.query.filter(OrderStat.bemail == get_jwt_identity()).all()
    return jsonify({"orders": [order.to_dict() for order in orders]})


@app.route("/order", methods=["POST"])
@role_check("buyer")
@require_auth
def order_delivered():
    idor = request.json.get("id")
    if not id:
        return error_msg("Missing order id.")

    try:
        idor = int(idor)
    except ValueError:
        return error_msg("Invalid order id.")
    if idor <= 0:
        return error_msg("Invalid order id.")

    order = OrderStat.query.filter(OrderStat.id == idor).first()
    if not order or order.status != "PENDING":
        return error_msg("Invalid order id.")

    order.status = "COMPLETED"
    database.session.commit()

    return Response(status=200)



