SQLAlchemy-Norm
===============

|Build Status|

Working in Progress. Normalize SQLAlchemy Object to Plain dict and list.

An example of a simple code:

.. code-block:: python

    from yourapp.database import Base
    from sqlalchemy_norm import Normalizable

    class User(Base, Normalizable):
        # ...

    me = User('Edward')
    norm = me.vars() # {"name": "Edward"}

If you like,

::

    python setup.py test


Usage
-----

Simple Model
~~~~~~~~~~~~

In model,

.. code-block:: python

    from datetime import datetime

    from sqlalchemy import Column, Integer, String, DateTime
    from sqlalchemy_norm import Normalizable

    from yourapp.database import Base


    class User(Base, Normalizable):
        __tablename__ = 'users'

        id = Column(Integer, primary_key=True)
        name = Column(String)
        nickname = Column(String)
        password = Column(String) # do not save password as plain string
        point = Column(Integer)
        created_at = Column(DateTime)

        # specify your dict strcutrue inside the model
        __excludes__ = ['password']
        __includes__ = ['display_name']

        @property
        def display_name(self):
            return "%s (%s)" % (self.nickname, self.name)

        def __init__(self, name, nickname=None, created_at=datetime.now()):
            self.name = name
            self.nickname = nickname
            self.created_at = created_at

Now we can use it like below:

.. code-block:: python

    from models import User

    me = User("Edward", "haruair")
    me.password = "strong password"
    me.point = 42

    print(me.vars())
    """
    {
      'id': 1,
      'point': 42,
      'name': 'Edward',
      'nickname': 'haruair',
      'created_at': '2016-01-01T00:00:00.123456',
      'display_name': 'haruair (Edward)'
    }
    """

    print(me.vars(includes=["password"], excludes=["display_name", "name", "created_at"]))
    # {'nickname': 'haruair', 'password': 'strong password', 'point': 100}

    print(me.vars(includes_only=["display_name"]))
    # {'display_name': 'haruair (Edward)'}


Complex Model
~~~~~~~~~~~~~

Relationship between models,

.. code-block:: python

    from sqlalchemy import ForeignKey
    from sqlalchemy.orm import relationship, backref

    class Address(Base, Normalizable):
        __tablename__ = 'addresses'
        id = Column(Integer, primary_key=True)
        email = Column(String, nullable=False)

        user_id = Column(Integer, ForeignKey('users.id'))
        user = relationship("User", backref=backref('addresses', order_by=id))

        def __init__(self, email):
            self.email = email


.. code-block:: python

    from models import User, Addresses
    from yourapp.database import session

    me = User("Edward", "haruair")

    me.addresses = [
        Address("edward@example.com"),
        Address("haruair@example.com")
    ]

    session.add(me)
    session.commit()

    print(me.vars(includes=["addresses"]))
    """
    {
      'id': 1,
      'addresses': [
        {'email': 'edward@example.com', 'id': 1, 'user_id': 1},
        {'email': 'haruair@example.com', 'id': 2, 'user_id': 1}
      ],
      'display_name': 'haruair (Edward)',
      'point': None,
      'nickname': 'haruair',
      'created_at': '2016-09-16T14:16:37.359005',
      'name': 'Edward'
    }
    """


Why?
----

When I tried to convert from SQLAlchemy object to JSON, it's not an easy job
than I thought. I wonder if I can get plain objects from SQLAlchemy, it will
be better than another way. SQLAlchemy already use ``__dict__`` internally, so
I made kind of similar thing.


Contribute
----------

I'm not good at python and I don't know pythonic code that much. If you have
any idea or opinion about the code, please leave an issue on the issue tracker.
Contributing the code is always welcome.


.. |Build Status| image:: https://travis-ci.org/haruair/sqlalchemy-norm.svg?branch=master
   :target: https://travis-ci.org/haruair/sqlalchemy-norm
