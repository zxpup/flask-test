from flask import Flask, render_template, Response, request, jsonify
import zmq
import json
from call_back_dispose import Dispose

config = dict()
config['clinet_ip'] = '192.168.8.145'
config['push_port'] = '5566'
config['req_port'] = '5567'
config['host'] = '192.168.8.146'
config['port'] = 3306
config['user'] = 'sa'
config['pwd'] = 'yq888888'
config['db'] = 'Cinderella'
dispose = Dispose(config)
app = Flask(__name__)


@app.route('/login', methods=['POST'])
def login():
    return jsonify(dispose.login(request.json))


@app.route('/accounts', methods=['POST'])
def register_account():
    return Response(
        json.dumps(dispose.register_account(request.json)),
        mimetype='application/json')


@app.route('/accounts/<account_id>/bank_card', methods=['PUT'])
def bind_bank_card(account_id=None):
    return Response(
        json.dumps(dispose.bind_bank_card(account_id, request.json)),
        mimetype='application/json')


@app.route('/accounts/<account_id>', methods=['GET'])
def get_account_info(account_id=None):
    return Response(
        json.dumps(dispose.get_account_info(account_id)),
        mimetype='application/json')


@app.route('/accounts/<account_id>/balance', methods=['GET'])
def get_account_balance(account_id=None):
    return jsonify(dispose.get_account_balance(account_id))


@app.route('/accounts/<account_id>/password', methods=['PUT'])
def reset_password(account_id=None):
    return Response(
        json.dumps(dispose.reset_password(account_id, request.json)),
        mimetype='application/json')


@app.route('/accounts/<account_id>/account-balance', methods=['PUT'])
def create_voucher(account_id=None):
    return Response(
        json.dumps(dispose.create_voucher(account_id, request.json)),
        mimetype='application/json')


@app.route('/agents/<account_id>/accounts', methods=['GET'])
def get_agent_info(account_id=None):
    return Response(
        json.dumps(dispose.get_agent_info(account_id, request.json)),
        mimetype='application/json')


@app.route('/agents', methods=['POST'])
def create_agents():
    return Response(
        json.dumps(dispose.create_agents(request.json)),
        mimetype='application/json')


@app.route('/cash-vouchers/<voucher_no>', methods=['PUT'])
def fund_approved(voucher_no=None):
    return Response(
        json.dumps(dispose.fund_approved(voucher_no, request.json)),
        mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8081)
