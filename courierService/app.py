import datetime

from web3 import Web3,HTTPProvider
from flask import Flask, request, Response, jsonify
from flask_jwt_extended import JWTManager
from web3.exceptions import ContractLogicError

from config.shopConfig import Configuration
from shopModels import *
from utils import error_msg
from utils.auth_utils import require_auth, role_check
from utils.blockchain_utils import send_owner_transaction, get_contract
import os
app = Flask(__name__)
app.config.from_object(Configuration)


database.init_app(app)
jwt = JWTManager(app=app)


@app.route("/orders_to_deliver", methods=["GET"])
@role_check("courier")
@require_auth
def get_orders():
    orders = OrderStat.query.filter(OrderStat.status == "CREATED").all()
    res = []
    for order in orders:
        res.append({"id": order.id, "email": order.bemail})

    return jsonify(orders=res)


@app.route("/pick_up_order", methods=["POST"])
@role_check("courier")
@require_auth
def pickup_order():
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
    if not order or order.status != "CREATED":
        return error_msg("Invalid order id.")


    w3 = Web3(HTTPProvider(f"http://{os.environ.get('BLOCKCHAIN_URL') or '127.0.0.1'}:8545"))
    address = request.json.get("address")

    if not address:
        return error_msg("Missing address.")

    try:
        address = w3.to_checksum_address(address)
    except Exception:
        return error_msg("Invalid address.")

    contract = get_contract(w3, order.address)
    contractFun = contract.functions.get_delivery(address)
    try:
      send_owner_transaction(w3, contractFun)
    except ContractLogicError as error:
        errl = error.message.split(" ")
        if errl[-1] == "CREATED":
            return error_msg("Transfer not complete.")
        return error_msg(error.message)

    order.status = "PENDING"
    database.session.commit()
    return Response(status=200)