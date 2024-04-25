import hashlib
import hmac
import secrets


class Hmac:
    def __init__(self, secret_key: str = "", hasher=hashlib.sha256) -> None:
        if not secret_key:
            secret_key = self.generate_secret_key()
        self.secret = secret_key
        self.hasher = hasher

    def calc(self, message: str) -> str:
        return hmac.new(self.secret.encode(), message.encode(), self.hasher).hexdigest()

    def generate_secret_key(self) -> str:
        return secrets.token_urlsafe(16)
