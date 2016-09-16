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
        name = sa.Column(sa.String)
        nickname = sa.Column(sa.String)
        point = sa.Column(sa.Integer)
        created_at = sa.Column(sa.DateTime)

        primary_address = relationship("Address", uselist=False)

        __includes__ = ['addresses']

        @property
        def display_name(self):
            return "%s (%s)" % (self.nickname, self.name)

        def __init__(self, name, created_at):
            self.name = name
            self.created_at = created_at

    return User

@pytest.fixture
def Address(Base):
    class Address(Base, Normalizable):
        __tablename__ = 'addresses'
        id = sa.Column(sa.Integer, primary_key=True)
        email = sa.Column(sa.String, nullable=False)

        user_id = sa.Column(sa.Integer, ForeignKey('users.id'))
        user = relationship("User", backref=backref('addresses', order_by=id))

        def __init__(self, email):
            self.email = email

    return Address

@pytest.fixture
def UserWithinAddresses(User, Address):
    me = User("Edward", datetime.now())
    addr1 = Address("edward@example.com")
    addr2 = Address("haruair@example.com")
    me.addresses = [ addr1, addr2 ]
    me.primary_address = addr1
    return me


class TestComplexNomarlizable():
    def test_type(self, UserWithinAddresses):
        norm = UserWithinAddresses.vars()
        assert isinstance(norm, dict)

    def test_complex_norm_list(self, UserWithinAddresses):
        firstEmail = UserWithinAddresses.addresses[0].email
        norm = UserWithinAddresses.vars()

        assert "addresses" in norm
        assert isinstance(norm["addresses"], list)
        assert len(norm["addresses"]) == len(UserWithinAddresses.addresses)
        assert norm["addresses"][0]["email"] == firstEmail

    def test_complex_norm_includes_only(self, UserWithinAddresses):
        norm = UserWithinAddresses.vars(includes_only=["name", "point"])

        assert "addresses" not in norm
        assert "nickname" not in norm
        assert "name" in norm
        assert "point" in norm

    def test_complex_norm_excludes(self, UserWithinAddresses):
        norm = UserWithinAddresses.vars(excludes=["name", "point"])

        assert "addresses" in norm
        assert "nickname" in norm
        assert "name" not in norm
        assert "point" not in norm

    def test_complex_norm_property(self, UserWithinAddresses):
        norm1 = UserWithinAddresses.vars()
        norm2 = UserWithinAddresses.vars(includes=["display_name"])

        assert "display_name" not in norm1
        assert "display_name" in norm2
        assert norm2["display_name"] == UserWithinAddresses.display_name

    def test_complex_norm_single_relation(self, UserWithinAddresses):
        primaryEmail = UserWithinAddresses.primary_address.email
        norm = UserWithinAddresses.vars(includes=["primary_address"])

        assert "primary_address" in norm
        assert norm["primary_address"]["email"] == primaryEmail
