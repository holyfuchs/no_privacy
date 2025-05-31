from typing import List, Tuple, Dict
import requests_cache
from .ens import address_from_ens, ens_from_address, other_ens_owned_by, domain_events
from .transactions import get_transactions
from .tokens import get_token_transfers


def create_graph(session: requests_cache.CachedSession, input: str):
    if input.endswith(".eth"):
        input = address_from_ens(session, input)
    if not input.startswith("0x") or len(input) != 42:
        return [], []
    ens = ens_from_address(session, input)
    other_ens_owned = other_ens_owned_by(session, input)
    addresses_with_domain_events = []
    for e in ens:
        addresses_with_domain_events.extend(domain_events(session, e))
    transactions = get_transactions(session, input)
    token_transfers = get_token_transfers(session, input)
    nodes = [
        {
            "id": 0,
            "label": "\n".join(ens),
            "group": 1,
            "size": 20,
            "address": input
        },
    ]
    edges = []
    addresses_with_domain_events = set(addresses_with_domain_events)
    if input in addresses_with_domain_events:
        addresses_with_domain_events.remove(input)
    for address in addresses_with_domain_events:
        add_address_to_nodes(nodes, edges, address, 1)
    for e in other_ens_owned:
        if e["address"]:
            add_address_to_nodes(nodes, edges, e["address"], 1, e["name"])
    top_interactions = count_transactions_by_address(transactions + token_transfers)[:10]
    max_amount = (top_interactions[1][1] + top_interactions[1][2]) / 2
    for i in top_interactions:
        add_address_to_nodes(nodes, edges, i[0], (i[1] + i[2]) / max_amount)
    for n in nodes:
        if n["label"].startswith("0x") and len(n["label"]) == 42:
            ens = ens_from_address(session, n["address"])
            if len(ens) > 0:
                nodes[nodes.index(n)]["label"] = ens[0]
    for e in edges:
        if e["from"] == e["to"]:
            del edges[edges.index(e)]
    return nodes, edges

def count_transactions_by_address(
        transactions: List[dict]) -> List[Tuple[str, int, int]]:
    transactions = [tx for tx in transactions if not tx["contract"]]
    address_counts: Dict[str, Tuple[int, int]] = {}

    for tx in transactions:
        if tx['from'] not in address_counts:
            address_counts[tx['from']] = (0, 0)
        if tx['to'] not in address_counts:
            address_counts[tx['to']] = (0, 0)

        from_in, from_out = address_counts[tx['from']]
        to_in, to_out = address_counts[tx['to']]

        address_counts[tx['from']] = (from_in, from_out + 1)
        address_counts[tx['to']] = (to_in + 1, to_out)

    result = [(addr, in_count, out_count)
              for addr, (in_count, out_count) in address_counts.items()]
    return sorted(result, key=lambda x: x[1] + x[2], reverse=True)


def add_address_to_nodes(nodes: List[dict], edges: List[dict], address: str, strength: int, label: str = None):
    node = next((a for a in nodes if a["address"] == address), None)
    if node is None:
        nodes.append({
            "id": len(nodes),
            "label": label if label else address,
            "group": 2,
            "size": 10,
            "address": address
        })
        node = nodes[-1]
    
    edge = next((e for e in edges if e["to"] == node["id"]), None)
    if edge is None:
        edges.append({
            "from": 0,
            "to": node["id"],
            "strength": strength
        })
    else:
        edges[edges.index(edge)]["strength"] += strength