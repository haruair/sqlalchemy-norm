"""
SQLAlchemy-Norm
---------------

Normalize SQLAlchemy Object to Plain dict and list
"""
from setuptools import setup

setup(
    name='SQLAlchemy-Norm',
    version='0.0.1',
    url='https://github.com/haruair/sqlalchemy-norm',
    license='BSD',
    author='Edward Kim',
    author_email='onward.edkim@gmail.com',
    description=(
        'Normalize SQLAlchemy Object'
    ),
    packages=['sqlalchemy_norm'],
    platforms='any',
    install_requires=[
        'SQLAlchemy>=0.9'
    ],
    setup_requires=[
        'pytest-runner'
    ],
    tests_require=[
        'pytest',
    ],
)

