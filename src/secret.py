import hashlib
import hmac
import secrets


def calc_hmac(secret: str, message: str) -> str:
    return hmac.new(secret.encode(), message.encode(), hashlib.sha256).hexdigest()


def generate_secret_key() -> str:
    return secrets.token_urlsafe(16)