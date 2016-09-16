SQLAlchemy-Norm
===============

Normalize SQLAlchemy Object to Plain dict and list.

Working in Progress.

An example of a simple code:

.. code-block:: python
   from database import Base
   from sqlalchemy_norm import Normalizable

   class User(Base, Normalizable):
       # ...

   me = User('Edward')
   norm = me.vars() # {"name": "Edward"}
