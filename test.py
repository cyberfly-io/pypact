from pypact.pact import Pact
import time
from datetime import datetime
api_host = "https://kadena2.app.runonflux.io/chainweb/0.0/mainnet01/chain/1/pact"
test_net = "https://api.testnet.chainweb.com/chainweb/0.0/testnet04/chain/1/pact"
pact = Pact()
amount = 10.0
key_pair = {'publicKey': '10375651f1ca0110468152bb8f47b7b8a469e36dfab1c83adf60cab84b5726d3',
            'secretKey': '18d3a823139cf60cab0b738e7605bb9e4a2f3ff245c270fa55d197f9b3c4c004',
            'clist': [{'name': 'coin.GAS', 'args': []},
                      {"name": "coin.TRANSFER",
                       'args': ['k:10375651f1ca0110468152bb8f47b7b8a469e36dfab1c83adf60cab84b5726d3',
                                'k:03df480e0b300c52901fdff265f0460913fea495f39972321698740536cc38e3', amount]}]}


cmd = {
    "pactCode": '(coin.transfer-create "k:10375651f1ca0110468152bb8f47b7b8a469e36dfab1c83adf60cab84b5726d3" "k:03df480e0b300c52901fdff265f0460913fea495f39972321698740536cc38e3" (read-keyset "ks")  10.0)',
    "envData": {
        "ks": {
             "pred": "keys-all",
             "keys": ["03df480e0b300c52901fdff265f0460913fea495f39972321698740536cc38e3"]
        }
    },
    "meta": pact.lang.mk_meta("k:"+key_pair.get('publicKey'), chain_id="1", gas_price=0.0000001, gas_limit=60000,
                              creation_time=time.time().__round__()-100, ttl=15000),
    "networkId": "testnet04",
    "nonce": datetime.now().isoformat(),
    "keyPairs": [key_pair]
}

result = pact.fetch.send(cmd, test_net)
print(result)