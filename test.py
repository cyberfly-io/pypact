
from pypact import tools

key_pair = {'publicKey': '10375651f1ca0110468152bb8f47b7b8a469e36dfab1c83adf60cab84b5726d3',
            'secretKey': '18d3a823139cf60cab0b738e7605bb9e4a2f3ff245c270fa55d197f9b3c4c004',
            }

result = tools.token_transfer("coin", "k:10375651f1ca0110468152bb8f47b7b8a469e36dfab1c83adf60cab84b5726d3",
                              "k:03df480e0b300c52901fdff265f0460913fea495f39972321698740536cc38e3",
                              "03df480e0b300c52901fdff265f0460913fea495f39972321698740536cc38e3", 2.0, key_pair, "1",
                              "testnet04")

print(result)
