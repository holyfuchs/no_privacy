import requests_cache
from dataclasses import dataclass
from typing import Optional, List, Dict, Any

CHAINS = [
    "eth",
    "base",
    "optimism",
    "arbitrum",
    "polygon",
    "gnosis",
    "scroll",
    "celo",
    "eth-sepolia",
    "eth-goerli",
    "base-sepolia",
    "optimism-sepolia",
    "arbitrum-sepolia",
    "scroll-sepolia",
    "gnosis-chiado",
    "celo-alfajores",
    "celo-baklava",
]


def get_chain_transactions(session: requests_cache.CachedSession, address: str,
                           chain: str) -> List[dict]:
    url = f"https://{chain}.blockscout.com/api/v2/addresses/{address}/transactions"
    params = {}
    items = []
    for _ in range(10):
        response = session.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        items.extend(data["items"])
        params = data["next_page_params"]
        if params is None:
            break
    items = [
        item for item in items
        if not item["from"]["is_contract"] and not item["to"]["is_contract"]
    ]
    items = [{
        "from": item["from"]["hash"],
        "from_ens": item["from"]["ens_domain_name"],
        "to": item["to"]["hash"],
        "to_ens": item["to"]["ens_domain_name"],
        "chain": chain,
        "timestamp": item["timestamp"],
    } for item in items]
    return items


def get_transactions(session: requests_cache.CachedSession,
                     address: str) -> List[dict]:
    transactions = []
    for chain in CHAINS:
        transactions.extend(get_chain_transactions(session, address, chain))
    return transactions


if __name__ == "__main__":
    import json
    from datetime import timedelta
    session = requests_cache.CachedSession('cache')
    address = "0x53C61cfb8128ad59244E8c1D26109252ACe23d14"
    transactions = get_transactions(session, address)
    print(json.dumps(transactions, indent=4))
