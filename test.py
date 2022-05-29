from pypact.pact import Pact
import time
from datetime import datetime
api_host = "https://kadena2.app.runonflux.io/chainweb/0.0/mainnet01/chain/1/pact"
test_net = "https://api.testnet.chainweb.com/chainweb/0.0/testnet04/chain/1/pact"
pact = Pact()
key_pair = {'publicKey': '10375651f1ca0110468152bb8f47b7b8a469e36dfab1c83adf60cab84b5726d3',
            'secretKey': '18d3a823139cf60cab0b738e7605bb9e4a2f3ff245c270fa55d197f9b3c4c004',
            }

# without namespace
print(pact.lang.mk_exp(module_and_function="coin.details",
                       account="k:10375651f1ca0110468152bb8f47b7b8a469e36dfab1c83adf60cab84b5726d3"))
# with namespace
print(pact.lang.mk_exp(module_and_function="flux.get-balance", namespace="runonflux",
                       account="k:10375651f1ca0110468152bb8f47b7b8a469e36dfab1c83adf60cab84b5726d3"))



