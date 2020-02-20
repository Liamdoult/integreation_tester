"""A setuptools based setup module.

Based on https://github.com/pypa/sampleproject/blob/master/setup.py
"""

from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='integration_tester',
    version='0.3.0',
    description='A Docker based service manager for testing in Python.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/liamdoult/',
    author=[
        "Liam Doult",
    ],
    author_email='doult98@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='ci integration testing',
    packages=find_packages(),
    python_requires='>=3.7, <4',
    install_requires=[
        'docker',
    ],
    setup_requires=['pytest-runner'],
    tests_require=[
        'pymongo',
        'pika',
        'pytest',
        'redis',
    ],
    test_suite='test',
)
