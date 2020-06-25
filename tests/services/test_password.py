from pydantic import SecretStr

from app.services import password


def test_hashing_roundtrip():
    test_string = "testing"
    hashed = password.get_hash(test_string)

    assert test_string != hashed

    assert password.verify(SecretStr(test_string), hashed)
