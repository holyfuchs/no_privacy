import requests_cache
from typing import List, Optional


def address_from_ens(session: requests_cache.CachedSession,
                     domain: str) -> Optional[str]:
    url = f"https://bens.services.blockscout.com/api/v1/1/domains/{domain}"
    response = session.get(url)
    data = response.json()
    if "resolved_address" not in data:
        return None
    return data["resolved_address"]["hash"]

def ens_from_address(session: requests_cache.CachedSession,
                     address: str) -> List[str]:
    url = f"https://bens.services.blockscout.com/api/v1/1/addresses:lookup"
    params = {
        "address": address,
        "only_active": "false",
        "resolved_to": "true",
        "owned_by": "false",
    }
    response = session.get(url, params=params)
    data = response.json()["items"]
    if len(data) == 0:
        return []
    return [item["name"] for item in data]


def other_ens_owned_by(session: requests_cache.CachedSession,
                       address: str) -> List[dict[str, Optional[str]]]:
    url = f"https://bens.services.blockscout.com/api/v1/1/addresses:lookup"
    params = {
        "address": address,
        "only_active": "false",
        "resolved_to": "false",
        "owned_by": "true",
    }
    response = session.get(url, params=params)
    data = response.json()["items"]

    other_ens_owned = []
    for item in data:
        resolved_address = item.get("resolved_address", {})
        if not resolved_address or resolved_address.get("hash") != address:
            other_ens_owned.append({
                "name": item["name"],
                "address": resolved_address.get("hash") if resolved_address else None
            })
    return other_ens_owned

def domain_events(session: requests_cache.CachedSession, domain: str):
    url = f"https://bens.services.blockscout.com/api/v1/1/domains/{domain}/events"
    response = session.get(url)
    data = response.json()["items"]
    connected_events = set()
    for event in data:
        action = event["action"]
        if action != "atomicMatch_" and action != "migrateAll":
            connected_events.add(event["from_address"]["hash"])
    return list(connected_events)

if __name__ == "__main__":
    import json
    session = requests_cache.CachedSession('cache', expire_after=3600)
    print(json.dumps(domain_events(session, "kartik.eth"), indent=4))
