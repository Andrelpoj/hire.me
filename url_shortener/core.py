import hashlib
import base64

def shorten_url(long_url):
    hashed = hashlib.md5(long_url.encode()).digest()
    b64 = base64.b64encode(hashed, altchars='~_'.encode())
    short_url = b64[:9].decode('ascii')

    return short_url 