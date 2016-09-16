from datetime import datetime

import pytest
import sqlalchemy as sa

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

from sqlalchemy_norm import Normalizable


@pytest.fixture
def User(Base):
    class User(Base, Normalizable):
        __tablename__ = 'users'
        id = sa.Column(sa.Integer, primary_key=True)
        username = sa.Column(sa.String)
        password = sa.Column(sa.String) # what?
        created_at = sa.Column(sa.DateTime)

        __excludes__ = ['password']
        __includes__ = ['secrets']

        def __init__(self, name, password):
            self.name = name
            self.password = password
            self.created_at = datetime.now()

    return User

@pytest.fixture
def Secret(Base):
    class Secret(Base, Normalizable):
        __tablename__ = 'addresses'
        id = sa.Column(sa.Integer, primary_key=True)
        message = sa.Column(sa.String, nullable=False)
        created_at = sa.Column(sa.DateTime)

        user_id = sa.Column(sa.Integer, ForeignKey('users.id'))
        user = relationship("User", backref=backref('secrets', order_by=id))

        __includes_only__ = ['created_at']

        def __init__(self, email):
            self.email = email
            self.created_at = datetime.now()

    return Secret

@pytest.fixture
def UserWithinSecrets(User, Secret):
    me = User("Edward", "SuperStrongPassword")
    me.secrets = [
        Secret("Super Duper Secret"),
        Secret("Secret Agency No 007")
    ]
    return me


class TestExtNomarlizable():

    def test_default_excludes(self, UserWithinSecrets):
        norm = UserWithinSecrets.vars()

        assert "password" not in norm
        assert isinstance(norm["secrets"], list)
        assert len(norm["secrets"]) == len(UserWithinSecrets.secrets)

        firstSecret = norm["secrets"][0]
        assert "message" not in firstSecret
        assert "created_at" in firstSecret

    def test_additional_includes(self, UserWithinSecrets):
        norm = UserWithinSecrets.vars(includes=["password"])

        assert "password" in norm
        assert isinstance(norm["password"], str)
        assert norm["password"] == UserWithinSecrets.password
