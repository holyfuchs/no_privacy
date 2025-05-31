import requests_cache
from datetime import timedelta
import json
from flask import Flask, jsonify, send_from_directory
from info import get_address_info
from ens import address_from_ens, ens_from_address, other_ens_owned_by, domain_events
from transactions import get_transactions
from tokens import get_token_transfers
from time_series import get_time_series
from graph import count_transactions_by_address
from typing import List, Tuple, Dict
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='../public')
CORS(app)
session = requests_cache.CachedSession('cache',
                                     expire_after=timedelta(days=3))

INPUT = "kartik.eth"

def analyse_address(session: requests_cache.CachedSession, input: str):
    if input.endswith(".eth"):
        input = address_from_ens(session, input)
    ens = ens_from_address(session, input)
    other_ens_owned = other_ens_owned_by(session, input)
    addresses_with_domain_events = domain_events(session, input)
    transactions = get_transactions(session, input)
    token_transfers = get_token_transfers(session, input)
    time_series = get_time_series(transactions, token_transfers)
    transaction_counts = count_transactions_by_address(transactions)
    
    return {
        "address": input,
        "ens": ens,
        "ens_owned": other_ens_owned,
        "domain_events": addresses_with_domain_events,
        "time_series": time_series,
        "transaction_counts": transaction_counts,
    }

@app.route('/api/time-data/<address>')
def time_data(address):
    print(address)
    if address.endswith(".eth"):
        address = address_from_ens(session, address)
    transactions = get_transactions(session, address)
    token_transfers = get_token_transfers(session, address)
    time_series = get_time_series(transactions, token_transfers, address)
    return jsonify(time_series)

@app.route('/api/graph/<address>')
def graph_data(address):
    result = analyse_address(session, address)
    return jsonify(result["transaction_counts"])
    
# Serve Frontend
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


if __name__ == "__main__":
    app.run(debug=True, port=5000)
