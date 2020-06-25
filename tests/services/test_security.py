from pydantic import SecretStr

from app.models.orm.user import User
from app.services import security
from app.services.password import get_hash


def test_authenticate_user(db):
    assert not security.authenticate_user(db, "test1", SecretStr("foobar"))

    user = User(username="test1", hashed_password=get_hash("foobar"))
    db.add(user)
    db.commit()

    assert security.authenticate_user(db, "test1", SecretStr("foobar"))

    assert not security.authenticate_user(db, "test2", SecretStr("foobar"))
    assert not security.authenticate_user(db, "test1", SecretStr("foobar2"))
