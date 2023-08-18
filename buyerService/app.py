from datetime import datetime
from json import JSONDecodeError

from web3 import Web3, HTTPProvider, Account
from flask import Flask, request, Response, jsonify
from flask_jwt_extended import JWTManager, get_jwt_identity
from sqlalchemy import and_
from web3.exceptions import ContractLogicError

from config.shopConfig import Configuration
from shopModels import *
from utils import error_msg
from utils.blockchain_utils import deploy_contract, get_contract, send_transaction
from utils.auth_utils import require_auth, role_check
import os

app = Flask(__name__)
app.config.from_object(Configuration)

database.init_app(app)
jwt = JWTManager(app=app)


@app.route("/search", methods=["GET"])
@role_check("customer")
@require_auth
def search_products():
    name = request.args.get("name", "")
    category = request.args.get("category", "")

    products = database.session.query(Product).join(Product.categories) \
        .filter(
        and_(Category.name.like(f"%{category}%"),
             Product.name.like(f"%{name}%"))
    ).order_by(Product.id.asc()).distinct()

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
@role_check("customer")
@require_auth
def order_product():
    reqs = request.json.get("requests")
    if not reqs:
        return error_msg("Field requests is missing.")

    o = OrderStat(bemail=get_jwt_identity(), status="CREATED", created=datetime.now())
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
            except Exception:
                return error_msg(f"Invalid product {f} for request number {i}.")
            if fields[f] <= 0:
                return error_msg(f"Invalid product {f} for request number {i}.")

    w3 = Web3(HTTPProvider(f"http://{os.environ.get('BLOCKCHAIN_URL') or '127.0.0.1'}:8545"))
    address = request.json.get("address")

    for i,p in enumerate(reqs):
        product = Product.query.filter(Product.id == p["id"]).first()
        if not product:
            return error_msg(f"Invalid product for request number {i}.")
        pos.append(ProductOrder(order=o, quantity=p["quantity"], product=product))
        price += product.price*p["quantity"]

    if not address:
        return error_msg("Field address is missing.")

    try:
        address = w3.to_checksum_address(address)
    except Exception:
        return error_msg("Invalid address.")

    o.address = deploy_contract(w3, address, int(price))
    o.price = price
    database.session.add(o)
    database.session.add_all(pos)
    database.session.commit()


    res = {"id": o.id}
    return jsonify(res)


@app.route("/status", methods=["GET"])
@role_check("customer")
@require_auth
def order_status():
    orders = OrderStat.query.filter(OrderStat.bemail == get_jwt_identity()).all()
    return jsonify({"orders": [order.to_dict() for order in orders]})


@app.route("/delivered", methods=["POST"])
@role_check("customer")
@require_auth
def order_delivered():
    w3 = Web3(HTTPProvider(f"http://{os.environ.get('BLOCKCHAIN_URL') or '127.0.0.1'}:8545"))

    idor = request.json.get("id")
    if not idor:
        return error_msg("Missing order id.")

    try:
        idor = int(idor)
    except Exception:
        return error_msg("Invalid order id.")
    if idor <= 0:
        return error_msg("Invalid order id.")

    order = OrderStat.query.filter(OrderStat.id == idor).first()
    if not order or order.status != "PENDING":
        return error_msg("Invalid order id.")

    keys = request.json.get("keys")
    if not keys:
        return error_msg("Missing keys.")

    passphrase = request.json.get("passphrase")
    if not passphrase:
        return error_msg("Missing passphrase.")
    try:
        keys = json.loads(keys)
    except JSONDecodeError:
        keys = request.json.get("keys")
        keys = keys.replace("'", '"')
        try:
            keys = json.loads(keys)
        except JSONDecodeError:
            return error_msg("Invalid credentials.")

    address = w3.to_checksum_address(keys["address"])
    try:
        private_key = Account.decrypt(keys, passphrase).hex()
    except Exception:
        return error_msg("Invalid credentials.")

    contract = get_contract(w3, order.address)
    balance = w3.eth.get_balance(address)
    if balance < int(order.price):
        return error_msg("Insufficient funds.")

    try:
        transaction = contract.functions.delivered().build_transaction({
            "from": address,
            "nonce": w3.eth.get_transaction_count(address),
            "gasPrice": 1
        })
        send_transaction(w3, private_key, transaction)
    except ContractLogicError as error:
        errl = error.message.split(" ")
        if errl[-1] == "customer!":
            return error_msg("Invalid customer account.")
        if errl[-1] == "CREATED":
            return error_msg("Transfer not complete.")
        if errl[-1] == "PAYED":
            return error_msg("Delivery not complete.")
        return error_msg(error.message)

    order.status = "COMPLETE"
    database.session.commit()
    return Response(status=200)

@app.route("/pay", methods=["POST"])
@role_check("customer")
@require_auth
def pay():

    w3 = Web3(HTTPProvider(f"http://{os.environ.get('BLOCKCHAIN_URL') or '127.0.0.1'}:8545"))
    idor = request.json.get("id")
    if not idor:
        return error_msg("Missing order id.")

    try:
        idor = int(idor)
    except Exception:
        return error_msg("Invalid order id.")
    if idor <= 0:
        return error_msg("Invalid order id.")

    order = OrderStat.query.filter(OrderStat.id == idor).first()
    if not order:
        return error_msg("Invalid order id.")

    keys = request.json.get("keys")
    if not keys:
        return error_msg("Missing keys.")

    passphrase = request.json.get("passphrase")
    if not passphrase:
        return error_msg("Missing passphrase.")

    try:
        keys = json.loads(keys)
    except JSONDecodeError:
        keys = request.json.get("keys")
        keys = keys.replace("'", '"')
        try:
            keys = json.loads(keys)
        except JSONDecodeError:
            return error_msg("Invalid credentials.")
    address = w3.to_checksum_address(keys["address"])
    try:
        private_key = Account.decrypt(keys, passphrase).hex()
    except Exception:
        return error_msg("Invalid credentials.")

    contract = get_contract(w3, order.address)

    balance = w3.eth.get_balance(address)

    print("BALANCE:  " + str(balance))
    if int(str(balance)) < int(order.price):
        return error_msg("Insufficient funds.")

    try:
        transaction = contract.functions.pay().build_transaction({
            "from": address,
            "value": int(order.price),
            "nonce": w3.eth.get_transaction_count(address),
            "gasPrice": 1
        })
        send_transaction(w3, private_key, transaction)
    except ContractLogicError:
        return error_msg("Transfer already complete.")

    return Response(status=200)




