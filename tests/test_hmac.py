from src.secret import Hmac


def test_hmac():
    hmac = Hmac(secret_key="123")
    assert (
        hmac.calc("1")
        == "ccc8c71905806db18c0241b58a8e36e949ab8a45961041b4226b2a4284568e69"
    )
    assert (
        hmac.calc("2")
        == "8b808a62f8893cf1ce0f44fb62b433e3c21a4f5605687689d9f0bb1a3524439b"
    )
    assert (
        hmac.calc("3")
        == "4c7a50b711a7d89ef1589cc551aa325d6aaea3cb8b151352f15aa3f3a52fc4f1"
    )
