
from pypact.pact import Pact
pubkey = 'd04bbd8f403e583248aa461896bd7518113f89b85c98f3d9596bbfbf30df0bcb'
msg='{\"pin_no\": \"16\", \"status\": \"on\", \"expiry_time\": 1661419001}'
sig = '902d00bc675e7631a836c1473e434ccd6fd3462051f581b555a2267f86bf006331e7e2711be051222274d6c1afe29a7fe532365a30f98f82ce7f1c91905c3f0a'
print(Pact().Crypto.verify(msg, pubkey, sig))