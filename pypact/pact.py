import base64
import hashlib
import json
from nacl.signing import SigningKey
from nacl import signing
from nacl.encoding import HexEncoder
import requests as rt
from datetime import datetime

from pypact import utils


class Pact:
    def __init__(self):
        self.crypto = self.Crypto()
        self.api = self.Api()
        self.lang = self.Lang()
        self.simple = self.Simple()
        self.fetch = self.Fetch()

    class Crypto:
        def __init__(self):
            pass

        @staticmethod
        def hex_to_bin(number):
            nomint = utils.hex_to_int(number)
            return utils.int_to_bin(nomint)

        @staticmethod
        def bin_to_hex(number):
            nomintb = utils.bin_to_int(number)
            return utils.int_to_hex(nomintb)

        @staticmethod
        def hash_bin(msg):
            hash2b = hashlib.blake2b(digest_size=32)
            hash2b.update(bytes(str(msg), encoding="utf-8"))
            return hash2b.digest()

        @staticmethod
        def b64_url_encoded_hash(bin):
            return base64.urlsafe_b64encode(bin).decode("utf-8").strip("=")

        @staticmethod
        def gen_key_pair():
            kp = SigningKey.generate()
            sk = kp.encode(encoder=HexEncoder).decode("utf-8")
            pk = kp.verify_key.encode(encoder=HexEncoder).decode("utf-8")
            return {"publicKey": pk, "secretKey": sk}

        @staticmethod
        def restore_key_from_secret(secret):
            kp = SigningKey(seed=secret, encoder=HexEncoder)
            return {"publicKey": kp.verify_key.encode(encoder=HexEncoder).decode("utf-8"), "secretKey": secret}

        @staticmethod
        def sign(msg, keypair):
            print("from sign")
            print(msg)
            hs_bin = Pact.Crypto.hash_bin(msg)
            hsh = Pact.Crypto.b64_url_encoded_hash(hs_bin)
            sig_bin = signing.SigningKey(seed=keypair['secretKey'],
                                         encoder=HexEncoder).sign(hs_bin, encoder=HexEncoder)
            return {"hash": hsh, "sig": sig_bin.signature.decode("utf-8"), "pubKey": keypair['publicKey']}

        @staticmethod
        def sign_map(msg, kp):
            print("from signmap")
            print(msg)
            hs_bin = Pact.Crypto.hash_bin(msg)
            hsh = Pact.Crypto.b64_url_encoded_hash(hs_bin)
            if "publicKey" in kp.keys() and "secretKey" in kp.keys():
                return Pact.Crypto.sign(msg, kp)
            else:
                return {"hash": hsh, "sig": None, "publicKey": kp['publicKey']}

        @staticmethod
        def attach_sig(msg, kp_array):
            print("from attachsig")
            print(msg)
            hs_bin = Pact.Crypto.hash_bin(msg)
            hsh = Pact.Crypto.b64_url_encoded_hash(hs_bin)
            if len(kp_array) == 0:
                return [{"hash": hsh, "sig": None}]
            sig_list = []
            for kp in kp_array:
                sig_list.append(Pact.Crypto.sign_map(msg, kp))
            return sig_list

    class Api:
        def __init__(self):
            pass

        @staticmethod
        def filter_sig(sig):
            s = sig.get('sig')
            if s is None:
                return {}
            return {"sig": sig.get('sig')}

        @staticmethod
        def mk_single_cmd(sigs, cmd):
            return {
                "hash": utils.pull_check_hashs(sigs),
                "sigs": list(map(utils.pull_sig, filter(Pact.Api.filter_sig, sigs))),
                "cmd": cmd
            }

        @staticmethod
        def prepare_exec_cmd(pact_code, env_data={}, meta={}, network_id=None,
                             nonce=datetime.now().isoformat(), key_pairs=[]):
            kp_array = utils.as_list(key_pairs)
            signers = list(map(utils.mk_signer, kp_array))
            cmd_json = {
                "networkId": network_id,
                "payload": {
                    "exec": {
                        "data": env_data,
                        "code": pact_code
                    }
                },
                "signers": signers,
                "meta": meta,
                "nonce": json.dumps(nonce)
            }
            cmd = json.dumps(cmd_json)
            sigs = Pact.Crypto.attach_sig(cmd, kp_array)
            return Pact.Api.mk_single_cmd(sigs, cmd)

        @staticmethod
        def prepare_cont_cmd(pact_id, rollback, step, proof=None, env_data={}, meta={},
                             network_id=None,
                             nonce=datetime.now().isoformat(), key_pairs=[]):
            kp_array = utils.as_list(key_pairs)
            signers = list(map(utils.mk_signer, kp_array))
            cmd_json = {
                "networkId": network_id,
                "payload": {
                    "cont": {
                        "proof": proof,
                        "pactId": pact_id,
                        "rollback": rollback,
                        "step": step,
                        "data": env_data
                    }
                },
                "signers": signers,
                "meta": meta,
                "nonce": json.dumps(nonce)
            }
            cmd = json.dumps(cmd_json)
            sigs = Pact.Crypto.attach_sig(cmd, kp_array)
            return Pact.Api.mk_single_cmd(sigs, cmd)

        def mk_public_send(cmds):
            return {"cmds": utils.as_list(cmds)}

    class Lang:
        def __init__(self):
            pass

        @staticmethod
        def mk_meta(sender, chain_id, gas_price, gas_limit, creation_time, ttl):
            return {"creationTime": creation_time, "ttl": ttl, "gasLimit":
                    gas_limit, "chainId": chain_id, "gasPrice": gas_price, "sender": sender}

        @staticmethod
        def mk_cap(role, description, name, args=[]):
            return {"role": role, "description": description, "cap": {
                "name": name,
                "args": args
            }}

        @staticmethod
        def mk_exp(module_and_function, namespace=None, **kwargs):
            if namespace:
                string = "("+namespace+"."+module_and_function+" "
            else:
                string = "("+module_and_function+" "
            for key, value in kwargs.items():
                string += json.dumps(value)
            return string+")"

    class Simple:
        def __init__(self):
            self.cont = self.Cont()
            self.exec = self.Exec()

        class Exec:
            def __init__(self):
                pass

            @staticmethod
            def prepare_exec_cmd(pact_code, env_data={}, meta={}, network_id=None,
                                 nonce=datetime.now().isoformat(), key_pairs=[]):
                kp_array = utils.as_list(key_pairs)
                signers = list(map(utils.mk_signer, kp_array))
                cmd_json = {
                    "networkId": network_id,
                    "payload": {
                        "exec": {
                            "data": env_data,
                            "code": pact_code
                        }
                    },
                    "signers": signers,
                    "meta": meta,
                    "nonce": json.dumps(nonce)
                }
                cmd = json.dumps(cmd_json)
                sigs = Pact.Crypto.attach_sig(cmd, kp_array)
                return Pact.Api.mk_single_cmd(sigs, cmd)

            @staticmethod
            def simple_exec_command(pact_code, env_data, meta, network_id, nonce, key_pairs):
                cmd = Pact.Simple.Exec.prepare_exec_cmd(pact_code, env_data, meta, network_id, nonce, key_pairs)
                return Pact.Api.mk_public_send(cmd)

        class Cont:
            def __init__(self):
                pass

            @staticmethod
            def prepare_cont_cmd(pact_id, rollback, step, proof=None, env_data={}, meta={},
                                 network_id=None,
                                 nonce=datetime.now().isoformat(), key_pairs=[]):
                kp_array = utils.as_list(key_pairs)
                signers = list(map(utils.mk_signer, kp_array))
                cmd_json = {
                    "networkId": network_id,
                    "payload": {
                        "cont": {
                            "proof": proof,
                            "pactId": pact_id,
                            "rollback": rollback,
                            "step": step,
                            "data": env_data
                        }
                    },
                    "signers": signers,
                    "meta": meta,
                    "nonce": json.dumps(nonce)
                }
                cmd = json.dumps(cmd_json)
                sigs = Pact.Crypto.attach_sig(cmd, kp_array)
                return Pact.Api.mk_single_cmd(sigs, cmd)

            @staticmethod
            def simple_cont_command(pact_id, rollback, step, proof, env_data, meta, network_id,
                                    nonce, key_pairs):
                cmd = Pact.Simple.Cont.prepare_cont_cmd(pact_id, rollback, step, proof,
                                                        env_data, meta, network_id, nonce, key_pairs)
                return Pact.Api.mk_public_send(cmd)

    class Fetch:
        def __init__(self):
            pass

        @staticmethod
        def simple_poll_req_from_exec(exec_msg):
            cmds = exec_msg.get('cmds')
            if cmds is None:
                raise TypeError("expected key 'cmds' in object: " + json.dumps(exec_msg))
            rks = []
            for cmd in cmds:
                hsh = cmd.get('hash')
                if hsh is None:
                    raise TypeError("malformed object, expected 'hash' key in every cmd: " + json.dumps(exec_msg))
                rks.append(hsh)
            return {"requestKeys": utils.unique(rks)}

        @staticmethod
        def simple_listen_req_from_exec(exec_msg):
            cmds = exec_msg.get('cmds')
            if cmds is None:
                raise TypeError("expected key 'cmds' in object: " + json.dumps(exec_msg))
            rks = []
            for cmd in cmds:
                hsh = cmd.get('hash')
                if hsh is None:
                    raise TypeError("malformed object, expected 'hash' key in every cmd: " + json.dumps(exec_msg))
                rks.append(hsh)
            return {"listen": rks[0]}

        @staticmethod
        def make_prepare_cmd(cmd):
            if cmd.get("type") == "cont":
                return Pact.Simple.Cont.prepare_cont_cmd(cmd['pactId'], cmd['rollback'], cmd['step'], cmd['proof'],
                                                         cmd['envData'], cmd['meta'], cmd['networkId'], cmd['nonce'],
                                                         cmd['keyPairs'])
            return Pact.Simple.Exec.prepare_exec_cmd(cmd['pactCode'], cmd['envData'], cmd['meta'], cmd['networkId'],
                                                     cmd['nonce'], cmd['keyPairs'])

        @staticmethod
        def fetch_send_raw(send_cmd, api_host):
            if api_host is None:
                raise Exception("No apiHost provided")
            send_cmds = list(map(Pact.Fetch.make_prepare_cmd, utils.as_list(send_cmd)))
            return rt.post(api_host + '/api/v1/send', json=Pact.Api.mk_public_send(send_cmds), headers=utils.get_headers(), timeout=10)

        @staticmethod
        def send(send_cmd, api_host):
            res = Pact.Fetch.fetch_send_raw(send_cmd, api_host)
            return utils.parse_res(res)

        @staticmethod
        def fetch_spv_raw(spv_cmd, api_host):
            if api_host is None:
                raise Exception("No apiHost provided")
            return rt.post(api_host + '/spv', json=spv_cmd, headers=utils.get_headers(), timeout=10)

        @staticmethod
        def spv(spv_cmd, api_host):
            res = Pact.Fetch.fetch_spv_raw(spv_cmd, api_host)

            return utils.parse_res(res)

        @staticmethod
        def fetch_local_raw(local_cmd, api_host):
            if api_host is None:
                raise Exception("No apiHost provided")
            local_data = Pact.Simple.Exec.prepare_exec_cmd(local_cmd['pactCode'], local_cmd['envData'],
                                                           local_cmd['meta'], local_cmd['networkId'],
                                                           local_cmd['nonce'], local_cmd['keyPairs'])

            return rt.post(api_host + '/api/v1/local', json=local_data, headers=utils.get_headers(), timeout=10)

        @staticmethod
        def local(local_cmd, api_host):
            res = Pact.Fetch.fetch_local_raw(local_cmd, api_host)
            return utils.parse_res(res)

        @staticmethod
        def fetch_poll_raw(poll_cmd, api_host):
            if api_host is None:
                raise Exception("No apiHost provided")
            return rt.post(api_host + '/api/v1/poll', json=poll_cmd, headers=utils.get_headers(), timeout=10)

        @staticmethod
        def poll(poll_cmd, api_host):
            res = Pact.Fetch.fetch_poll_raw(poll_cmd, api_host)
            return utils.parse_res(res)

        @staticmethod
        def fetch_listen_raw(listen_cmd, api_host):
            if api_host is None:
                raise Exception("No apiHost provided")
            print(listen_cmd)
            return rt.post(api_host + '/api/v1/listen', json=listen_cmd, headers=utils.get_headers(), timeout=10)

        @staticmethod
        def listen(listen_cmd, api_host):
            res = Pact.Fetch.fetch_listen_raw(listen_cmd, api_host)
            return utils.parse_res(res)

        @staticmethod
        def send_signed(signed_cmd, api_host):
            cmd = {"cmds": [signed_cmd]}
            res = rt.post(api_host + '/api/v1/send', json=cmd, headers=utils.get_headers(), timeout=10)
            return res.json()

