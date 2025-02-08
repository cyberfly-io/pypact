from pypact.pact import Pact
import time
from datetime import datetime

pact = Pact()


def get_api_host(network_id, chain_id):

    hosts = {
        "mainnet01": "https://api.testnet.chainweb.com/chainweb/0.0/testnet04/chain/{}/pact".format(chain_id),
        "testnet04": "https://api.chainweb.com/chainweb/0.0/mainnet01/chain/{}/pact".format(chain_id)
    }
    return hosts[network_id]


def token_transfer(token_address: str, sender_account: str, receiver_account: str, receiver_public_key: str,
                   amount: float, key_pair: dict, chain_id: str, network_id: str ="mainnet01",):

    api_host = get_api_host(network_id, chain_id)

    if token_address != "coin":
        code = pact.lang.mk_exp(module_and_function='{}.transfer-create'.format(token_address.split('.')[1]),
                                namespace=token_address.split('.')[0], sender_account=sender_account,
                                receiver_account=receiver_account, keyset='(read-keyset "ks")', amount=amount)
    else:
        code = pact.lang.mk_exp(module_and_function='coin.transfer-create',
                                sender_account=sender_account, receiver_account=receiver_account,
                                keyset='(read-keyset "ks")', amount=amount)
    key_pair.update(clist=[
                                {'name': 'coin.GAS', 'args': []},
                                { "name": '{}.TRANSFER'.format(token_address), "args": [sender_account,
                                           receiver_account, amount] }
          ])

    cmd = {
        "pactCode": code,
        "envData": {
            "ks": {
                "pred": "keys-all",
                "keys": [receiver_public_key]
            }
        },
        "meta": pact.lang.mk_meta("k:" + key_pair.get('publicKey'), chain_id=chain_id, gas_price=0.0000001,
                                  gas_limit=60000, creation_time=time.time().__round__() - 100, ttl=15000),
        "networkId": network_id,
        "nonce": datetime.now().isoformat(),
        "keyPairs": [key_pair]
    }
    return pact.fetch.send(cmd, api_host)


def get_contract_code(namespace_dot_module, network_id, chain_id):
    cmd = {
        "pactCode": '(describe-module "{}")'.format(namespace_dot_module),
        "envData": {},
        "meta": pact.lang.mk_meta("not real", chain_id=chain_id, gas_price=0.0000001, gas_limit=60000,
                                  creation_time=time.time().__round__(), ttl=5000),
        "networkId": network_id,
        "nonce": datetime.now().isoformat(),
        "keyPairs": []
    }

    result = pact.fetch.local(cmd, get_api_host(network_id, chain_id))

    print(result)
