import json


def bin_to_int(number):
    """converts binary to integer"""
    number = str(number)
    return int(number, 2)


def int_to_bin(number):
    number = int(number)
    return int(bin(number)[2:])


def hex_to_int(number):
    number = str(number)
    return int(number, 16)


def int_to_hex(number):
    number = int(number)
    return str(hex(number)[2:])


def as_list(single_or_list):
    if isinstance(list, single_or_list):
        return single_or_list
    return [single_or_list]


def mk_signer(kp):
    if kp.get('clist'):
        return {"clist": as_list(kp.clist), "pubKey": kp.get("public_key")}
    return {"pubKey": kp.get('public_key')}


def pull_sig(s):
    if s.get('sig') is None:
        raise TypeError("Expected to find keys of name 'sig' in " + json.dumps(s))
    return {"sig": s.get('sig')}


def pull_check_hashs(sigs):
    hsh = sigs[0].get('hash')
    for i, sig in enumerate(sigs):
        if sigs[i].get('hash') != hsh:
            raise ValueError("Sigs for different hashes found: " + json.dumps(sigs))
    return hsh


def unique(arr):
    return list(set(arr))


def get_headers():
    return {"Content-Type": "application/json"}


def parse_res(raw):

    if raw.ok:
        return raw.json()
    return raw.text
