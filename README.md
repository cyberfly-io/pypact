
## Usage

Listen:

```python
from pypact.pact import Pact

pact = Pact()

print(pact.fetch.fetch_listen({"listen": "bTRFmTts8VVNGMVvzKfztoTFwVSrCAiTgakH-PG_LLI"}, "https://kadena2.app.runonflux.io/chainweb/0.0/mainnet01/chain/1/pact"))
```

Poll:

```python
from pypact.pact import Pact

api_host = "https://kadena2.app.runonflux.io/chainweb/0.0/mainnet01/chain/1/pact"

pact = Pact()

print(pact.fetch.fetch_poll({"requestKeys": ["bTRFmTts8VVNGMVvzKfztoTFwVSrCAiTgakH-PG_LLI"]}, api_host))

```

