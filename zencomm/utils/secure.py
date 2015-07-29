import base64
import M2Crypto

#generate session id
def generate_session_id(num_bytes=16):
    return base64.b64encode(M2Crypto.m2.rand_bytes(num_bytes))
