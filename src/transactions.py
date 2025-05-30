import requests_cache
from dataclasses import dataclass
from typing import Optional, List, Dict, Any

@dataclass
class AddressInfo:
    block_number_balance_updated_at: int
    coin_balance: str
    creation_transaction_hash: Optional[str]
    creator_address_hash: Optional[str]
    ens_domain_name: Optional[str]
    exchange_rate: str
    has_beacon_chain_withdrawals: bool
    has_logs: bool
    has_token_transfers: bool
    has_tokens: bool
    has_validated_blocks: bool
    hash: str
    implementations: List[Any]
    is_contract: bool
    is_scam: bool
    is_verified: bool
    metadata: Optional[Dict[str, Any]]
    name: Optional[str]
    private_tags: List[Any]
    proxy_type: Optional[str]
    public_tags: List[Any]
    token: Optional[Any]
    watchlist_address_id: Optional[int]
    watchlist_names: List[str]

def get_address_info(session: requests_cache.CachedSession, address: str) -> AddressInfo:
    url = f"https://eth.blockscout.com/api/v2/addresses/{address}"
    headers = {
        "accept": "application/json"
    }
    
    response = session.get(url, headers=headers)
    data = response.json()
    return AddressInfo(**data)

if __name__ == "__main__":
    address = "0x53C61cfb8128ad59244E8c1D26109252ACe23d14"
    print(get_address_info(address))
