from . import read_file
import os
from web3 import Web3, Account
def get_contract_files():
    bytecode = read_file("./solidity/output/Request.bin")
    abi = read_file("./solidity/output/Request.abi")
    return bytecode, abi

def deploy_contract(w3: Web3, address, price):
    bytecode, abi = get_contract_files()
    owner_private_key = os.environ.get("OWNER_PRIVATE_KEY")
    owner_address = Account.from_key(owner_private_key).address
    contract = w3.eth.contract(bytecode=bytecode, abi=abi)

    transaction = contract.constructor(address, price).build_transaction(
        {
            "from": owner_address,
            "nonce": w3.eth.get_transaction_count(owner_address),
            "gasPrice": 1
        }
    )
    transaction["gasPrice"] = w3.eth.estimate_gas(transaction)

    signed_transaction = w3.eth.account.sign_transaction(transaction, owner_private_key)
    transaction_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)

    return receipt.contractAddress

def get_contract(w3: Web3, address):
    _, abi = get_contract_files()
    contract = w3.eth.contract(address=address, abi=abi)

    return contract

def send_owner_transaction(w3: Web3, cont_fn):

    owner_private_key = os.environ.get("OWNER_PRIVATE_KEY")
    owner_address = Account.from_key(owner_private_key).address

    transaction = cont_fn.build_transaction({
        "from": owner_address,
        "nonce": w3.eth.get_transaction_count(owner_address),
        "gasPrice": 1
    })
    transaction["gasPrice"] = w3.eth.estimate_gas(transaction)

    signed_transaction = w3.eth.account.sign_transaction(transaction, owner_private_key)
    transaction_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)

def send_transaction(w3: Web3, private_key, transaction):
    transaction["gasPrice"] = w3.eth.estimate_gas(transaction)

    signed_transaction = w3.eth.account.sign_transaction(transaction, private_key)
    transaction_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)
