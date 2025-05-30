import requests_cache
from datetime import timedelta

from info import get_address_info
from ens import address_from_ens, ens_from_address, other_ens_owned_by

session = requests_cache.CachedSession('cache', expire_after=timedelta(hours=1))

# INPUT = "0x71B5b8Ec4D724849E76954A1475930dcE9c4B994"
INPUT = "kartik.eth"

def create_graph(session: requests_cache.CachedSession, input: str):
    if input.endswith(".eth"):
        input = address_from_ens(session, input)
    ens = ens_from_address(session, input)
    other_ens_owned = other_ens_owned_by(session, input)
    info = get_address_info(session, input)
    return {
        "address": input,
        "ens": ens,
        "ens_owned": other_ens_owned,
        # "info": info,
    }

if __name__ == "__main__":
    result = create_graph(session, INPUT)
    import json
    print(json.dumps(result, indent=4))
    print(json.dumps(domain_info(session, INPUT), indent=4))