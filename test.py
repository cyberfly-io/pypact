from pypact.pact import Pact

api_host = "https://kadena2.app.runonflux.io/chainweb/0.0/mainnet01/chain/1/pact"
test_net = "https://api.testnet.chainweb.com/chainweb/0.0/testnet04/chain/1/pact"
pact = Pact()
key_pair = {'publicKey': '10375651f1ca0110468152bb8f47b7b8a469e36dfab1c83adf60cab84b5726d3',
            'secretKey': '18d3a823139cf60cab0b738e7605bb9e4a2f3ff245c270fa55d197f9b3c4c004',
            }

pact = Pact()
cap = pact.lang.mk_cap("Coin Transfer", "Capability to transfer designated amount of coin from sender to receiver",
                       "coin.TRANSFER", ["sender_account", "receiver_account", 10.0])
print(cap)
