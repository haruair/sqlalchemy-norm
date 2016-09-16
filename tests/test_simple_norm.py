from datetime import datetime

import pytest
import sqlalchemy as sa

from sqlalchemy_norm import Normalizable


@pytest.fixture
def User(Base):
    class User(Base, Normalizable):
        __tablename__ = 'users'
        id = sa.Column(sa.Integer, primary_key=True)
        name = sa.Column(sa.String)
        nickname = sa.Column(sa.String)
        point = sa.Column(sa.Integer)
        created_at = sa.Column(sa.DateTime)

        def __init__(self, name, created_at):
            self.name = name
            self.created_at = created_at

    return User

@pytest.fixture
def BasicUser(User):
    me = User("Edward", datetime.now())
    me.point = 100
    return me

class TestNomarlizable():
    def test_basic_norm(self, BasicUser):
        norm = BasicUser.vars()
        assert isinstance(norm, dict)

    def test_basic_norm_str(self, BasicUser):
        norm = BasicUser.vars()
        assert "name" in norm
        assert isinstance(norm["name"], str)
        assert norm["name"] == "Edward"

    def test_basic_norm_int(self, BasicUser):
        norm = BasicUser.vars()
        assert "point" in norm
        assert isinstance(norm["point"], int)
        assert norm["point"] == 100

    def test_basic_norm_none(self, BasicUser):
        norm = BasicUser.vars()
        assert "nickname" in norm
        assert norm["nickname"] is None

    def test_basic_norm_datetime(self, BasicUser):
        norm = BasicUser.vars()
        assert "created_at" in norm
        assert BasicUser.created_at.isoformat() == norm["created_at"]
