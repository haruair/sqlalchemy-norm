SQLAlchemy-Norm
===============

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
