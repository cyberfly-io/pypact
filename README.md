
## Usage

### Install:

```shell
pip3 install pypact-lang
```

### note: secrets used in this example is for demo purpose only


Make pact expression:

```python
from pypact.pact import Pact

pact = Pact()

# without namespace
print(pact.lang.mk_exp(module_and_function="coin.details",
                       account="k:10375651f1ca0110468152bb8f47b7b8a469e36dfab1c83adf60cab84b5726d3"))
# with namespace
print(pact.lang.mk_exp(module_and_function="flux.get-balance", namespace="runonflux",
                       account="k:10375651f1ca0110468152bb8f47b7b8a469e36dfab1c83adf60cab84b5726d3"))
```


Make caps:

```python
from pypact.pact import Pact

pact = Pact()
cap = pact.lang.mk_cap("Coin Transfer", "Capability to transfer designated amount of coin from sender to receiver",
                       "coin.TRANSFER", ["sender_account", "receiver_account", 10.0])
print(cap)
```

Listen:

```python
from pypact.pact import Pact

pact = Pact()

print(pact.fetch.listen({"listen": "bTRFmTts8VVNGMVvzKfztoTFwVSrCAiTgakH-PG_LLI"}, "https://kadena2.app.runonflux.io/chainweb/0.0/mainnet01/chain/1/pact"))
```

Poll:

```python
from pypact.pact import Pact

api_host = "https://kadena2.app.runonflux.io/chainweb/0.0/mainnet01/chain/1/pact"

pact = Pact()

print(pact.fetch.poll({"requestKeys": ["bTRFmTts8VVNGMVvzKfztoTFwVSrCAiTgakH-PG_LLI"]}, api_host))

```

Generate keypair:

```python
from pypact.pact import Pact

pact = Pact()

key_pair = pact.crypto.gen_key_pair()

print(key_pair)
```


Restore public key from secret key:

```python
from pypact.pact import Pact

pact = Pact()

key_pair = pact.crypto.restore_key_from_secret("18d3a823139cf60cab0b738e7605bb9e4a2f3ff245c270fa55d197f9b3c4c004")

print(key_pair)
```

Sign:

```python
from pypact.pact import Pact

pact = Pact()

key_pair = {'publicKey': '10375651f1ca0110468152bb8f47b7b8a469e36dfab1c83adf60cab84b5726d3', 'secretKey': '18d3a823139cf60cab0b738e7605bb9e4a2f3ff245c270fa55d197f9b3c4c004'}

sig = pact.crypto.sign("message to be signed", key_pair)

print(sig)
```

Local Read:

```python
from pypact.pact import Pact
import time
from datetime import datetime
api_host = "https://kadena2.app.runonflux.io/chainweb/0.0/mainnet01/chain/1/pact"

pact = Pact()

cmd = {
    "pactCode": '(coin.details "k:99cb7008d7d70c94f138cc366a825f0d9c83a8a2f4ba82c86c666e0ab6fecf3a")',
    "envData": {},
    "meta": pact.lang.mk_meta("not real", chain_id="1", gas_price=0.0000001, gas_limit=60000,
                              creation_time=time.time().__round__(), ttl=5000),
    "networkId": "mainnet01",
    "nonce": datetime.now().isoformat(),
    "keyPairs": []
}

result = pact.fetch.local(cmd, api_host)

print(result)
```

Make transaction:

```python
from pypact.pact import Pact
import time
from datetime import datetime

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
```

tools token transfer example:

```python
from pypact import tools

key_pair = {'publicKey': '10375651f1ca0110468152bb8f47b7b8a469e36dfab1c83adf60cab84b5726d3',
            'secretKey': '18d3a823139cf60cab0b738e7605bb9e4a2f3ff245c270fa55d197f9b3c4c004',
            }

result = tools.token_transfer("coin", "k:10375651f1ca0110468152bb8f47b7b8a469e36dfab1c83adf60cab84b5726d3",
                              "k:03df480e0b300c52901fdff265f0460913fea495f39972321698740536cc38e3",
                              "03df480e0b300c52901fdff265f0460913fea495f39972321698740536cc38e3", 2.0, key_pair, "1",
                              "testnet04")

print(result)

```