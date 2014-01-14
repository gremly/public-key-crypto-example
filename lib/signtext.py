#!/usr/bin/env python

from M2Crypto import RSA
import hashlib
import base64

from config import PRIVATE_KEY, ENCODED_RESULT

def load_key():
    """
    Given key path loads as a
    RSA private key object.
    """
    pkey = RSA.load_key(PRIVATE_KEY)
    return pkey


def sign_text(text, private_key):
    """
    Recieves a clear text as parameter
    and a private key object, loaded
    from a system file.
    """
    digest = hashlib.new('sha256', text).digest()
    return private_key.sign(digest)


def main(text):
    """
    Manage load key, signature creation
    and returns base64 encoded result if
    configured.
    """
    pkey = load_key()
    signed = sign_text(text, pkey)

    if ENCODED_RESULT:
        signed = base64.b64encode(signed)

    return signed 


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        text = sys.argv[1]
        print main(text)
    else:
        print "Usage: signtext.py 'This is a clear text that will be signed.'"

