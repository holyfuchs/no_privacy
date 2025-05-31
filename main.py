import requests_cache
from datetime import timedelta
import json
from flask import Flask, jsonify, send_from_directory
from typing import List, Tuple, Dict
from flask_cors import CORS
import os
from asgiref.wsgi import WsgiToAsgi

from src.info import get_address_info
from src.ens import address_from_ens, ens_from_address, other_ens_owned_by, domain_events
from src.transactions import get_transactions
from src.tokens import get_token_transfers
from src.time_series import get_time_series
from src.graph import create_graph

app = Flask(__name__)
CORS(app)
session = requests_cache.CachedSession('cache',
                                     expire_after=timedelta(days=3))

@app.route('/api/time-data/<address>')
def time_data(address):
    if address.endswith(".eth"):
        address = address_from_ens(session, address)
    transactions = get_transactions(session, address)
    token_transfers = get_token_transfers(session, address)
    time_series = get_time_series(transactions, token_transfers, address)
    return jsonify(time_series)

@app.route('/api/graph/<address>')
def graph_data(address):    
    nodes, edges = create_graph(session, address)
    max_strength = max(edge["strength"] for edge in edges)
    for e in edges:
        e["width"] = e["strength"] * 10 / max_strength
        e["length"] = 1 / (e["strength"] / max_strength) * 10
        del e["strength"]
    for n in nodes:
        if n["id"] == 0:
            continue
        if len(n["label"]) > 10 and n["label"].startswith("0x"):
            n["label"] = n["label"][:6] + "..." + n["label"][-4:]

    return jsonify({"nodes": nodes, "edges": edges})
    
# Serve Frontend
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists('public' + '/' + path):
        return send_from_directory('public', path)
    else:
        return send_from_directory('public', 'index.html')


if __name__ == "__main__":
    app.run(debug=True, port=4321)

app = WsgiToAsgi(app)
