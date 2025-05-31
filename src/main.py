import requests_cache
from datetime import timedelta
import json
from info import get_address_info
from ens import address_from_ens, ens_from_address, other_ens_owned_by, domain_events
from transactions import get_transactions
from typing import List, Tuple, Dict

session = requests_cache.CachedSession('cache',
                                       expire_after=timedelta(days=3))

# INPUT = "0x71B5b8Ec4D724849E76954A1475930dcE9c4B994"
INPUT = "kartik.eth"

def count_transactions_by_address(transactions: List[dict]) -> List[Tuple[str, int, int]]:
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

def create_graph(session: requests_cache.CachedSession, input: str):
    if input.endswith(".eth"):
        input = address_from_ens(session, input)
    ens = ens_from_address(session, input)
    other_ens_owned = other_ens_owned_by(session, input)
    addresses_with_domain_events = domain_events(session, input)
    transactions = get_transactions(session, input)
    transaction_counts = count_transactions_by_address(transactions)
    return {
        "address": input,
        "ens": ens,
        "ens_owned": other_ens_owned,
        "domain_events": addresses_with_domain_events,
        "transaction_counts": transaction_counts,
    }


if __name__ == "__main__":
    result = create_graph(session, INPUT)
    print(json.dumps(result, indent=2))
