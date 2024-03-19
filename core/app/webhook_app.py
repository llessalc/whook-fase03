import requests
from flask import Flask, jsonify, request
from os import getenv

from core.models import payments
from core.models import orders
from core.database import webhook_db as db

app = Flask(__name__)

app.secret_key = getenv('APP_SECRET_KEY', 'testeXXX')
FLAG_DEBUG = getenv('FLAG_DEBUG', True)
PAGAMENTO_CONFIRMA_URL = getenv('PAGAMENTO_CONFIRMA_URL',
                                'http://pagamento-api.g58food.corp/gerenciamento-pagamento/pagamento/confirma/')


@app.route("/whorder", methods=["POST"])
def whorder():
    request_json = request.get_json(force=True)
    print(f'REQUEST JSON: {request_json}')
    print(f'request_json["order_id"] = {request_json["order_id"]}')
    print(f'request_json["order_qtd"] = {request_json["order_qtd"]}')
    print(f'request_json["order_value"] = {request_json["order_value"]}')

    ## Ao criar o pedido o webhook sera chamado para registrar este na base
    order = orders.Orders(
        order_id=request_json["order_id"],
        order_qtd=request_json["order_qtd"],
        order_value=request_json["order_value"],
    )

    db.init_db()
    db.db_session.add(order)
    db.db_session.commit()

    response = {"status": 200, "return": f'{request_json}'}
    return jsonify(response)


@app.route("/whpay", methods=["POST"])
def whpay():
    request_json = request.get_json(force=True)
    print(f'REQUEST JSON: {request_json}')
    print(f'request_json["payment_id"] = {request_json["payment_id"]}')
    print(f'request_json["type"] = {request_json["type"]}')
    print(f'request_json["user_id"] = {request_json["user_id"]}')
    print(f'request_json["api_version"] = {request_json["api_version"]}')
    print(f'request_json["action"] = {request_json["action"]}')
    print(f'request_json["qr_code"] = {request_json["qr_code"]}')

    payment = payments.Payments(
        payment_id=request_json["payment_id"],
        type=request_json["type"],
        user_id=request_json["user_id"],
        api_version=request_json["api_version"],
        action=request_json["action"],
        qr_code=request_json["qr_code"]
    )

    db.init_db()
    db.db_session.add(payment)
    db.db_session.commit()

    ## Chamar api de pagamento para confirmar a transacao
    resp = requests.post(PAGAMENTO_CONFIRMA_URL, json={
        "qr_code": payment.qr_code
    })

    response = {"status": 200, "return": f'{request_json}', "confirm": f'{resp}'}
    return jsonify(response)


@app.route("/health-check", methods=["GET"])
def healthcheck():
    response = {
        "status": 200,
        "version": "v0.2a"
    }
    return jsonify(response)


def __init__():
    print(f'iniciando app...')
    app.run(host='0.0.0.0', port=5000, debug=FLAG_DEBUG)
