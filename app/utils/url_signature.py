import base64
import hashlib
import hmac

from app.settings.globals import IMAGE_PROXY_KEY, IMAGE_PROXY_SALT


class UrlSignature:
    def __init__(self):
        self.key = bytes.fromhex(IMAGE_PROXY_KEY)
        self.salt = bytes.fromhex(IMAGE_PROXY_SALT)

    def sign_path(self, path: str) -> str:
        if not self.key or not self.salt:
            return ""
        path_encoded = path.encode()
        digest = hmac.new(
            self.key, msg=self.salt + path_encoded, digestmod=hashlib.sha256
        ).digest()
        protection = base64.urlsafe_b64encode(digest).rstrip(b"=")
        protected_url = b"%s%s" % (protection, path_encoded,)
        return protected_url.decode()


url_signature = UrlSignature()
