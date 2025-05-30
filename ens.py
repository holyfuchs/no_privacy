import requests_cache

def address_from_ens(session: requests_cache.CachedSession, domain: str) -> str:
    url = f"https://bens.services.blockscout.com/api/v1/1/domains/{domain}"
    response = session.get(url)
    data = response.json()
    return data["resolved_address"]["hash"]
