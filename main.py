import requests_cache
from datetime import timedelta

from info import get_address_info
from ens import address_from_ens
session = requests_cache.CachedSession('cache', expire_after=timedelta(hours=1))

# INPUT = "0x71B5b8Ec4D724849E76954A1475930dcE9c4B994"
INPUT = "qqqwe.eth"

def create_graph(session: requests_cache.CachedSession, input: str):
    if input.endswith(".eth"):
        input = address_from_ens(session, input)
    info = get_address_info(session, input)
    return {
        "address": input,
    }

if __name__ == "__main__":
    result = create_graph(session, INPUT)
    print(result)