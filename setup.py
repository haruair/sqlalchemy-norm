"""
SQLAlchemy-Norm
---------------

Normalize SQLAlchemy Object to Plain dict and list
"""
from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='SQLAlchemy-Norm',
    version='0.0.4',
    url='https://github.com/haruair/sqlalchemy-norm',
    license='BSD',
    author='Edward Kim',
    author_email='onward.edkim@gmail.com',
    description=(
        'Normalize SQLAlchemy Object to Plain dict and list'
    ),
    long_description=long_description,
    packages=['sqlalchemy_norm'],
    platforms='any',
    install_requires=[
        'SQLAlchemy>=0.9'
    ],
    setup_requires=[
        'pytest-runner'
    ],
    tests_require=[
        'pytest'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
