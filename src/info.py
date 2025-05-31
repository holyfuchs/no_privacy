import requests_cache
from dataclasses import dataclass
from typing import Optional, List, Dict, Any

def get_address_info(session: requests_cache.CachedSession, address: str):
    url = f"https://eth.blockscout.com/api/v2/addresses/{address}"
    headers = {
        "accept": "application/json"
    }
    
    response = session.get(url, headers=headers)
    data = response.json()
    return data

if __name__ == "__main__":
    address = "0x53C61cfb8128ad59244E8c1D26109252ACe23d14"
    print(get_address_info(address))
