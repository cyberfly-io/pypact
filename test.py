from pypact.pact import Pact
import time
import json
from datetime import datetime
api_host = "https://kadena2.app.runonflux.io/chainweb/0.0/mainnet01/chain/1/pact"

pact = Pact()

#key_pair = {'publicKey': '10375651f1ca0110468152bb8f47b7b8a469e36dfab1c83adf60cab84b5726d3', 'secretKey': '18d3a823139cf60cab0b738e7605bb9e4a2f3ff245c270fa55d197f9b3c4c004'}


cmd = {
    "pactCode": '(coin.details "k:10375651f1ca0110468152bb8f47b7b8a469e36dfab1c83adf60cab84b5726d3")',
    "envData": {},
    "meta": pact.lang.mk_meta("not real", chain_id="1", gas_price=0.0000001, gas_limit=60000,
                              creation_time=time.time().__round__(), ttl=5000),
    "networkId": "mainnet01",
    "nonce": json.dumps(datetime.now().isoformat()),
    "keyPairs": []
}

result = pact.fetch.local(cmd, api_host)

print(result)
