import pytest
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

@pytest.fixture
def Base():
    return declarative_base()

