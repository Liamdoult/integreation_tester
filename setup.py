""" A setuptools based setup module. """
from setuptools import setup, find_packages
from os import path

setup_file_location = path.abspath(path.dirname(__file__))
with open(path.join(setup_file_location, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='integration_tester',
    version='0.5.1',
    description='A Docker based service manager for testing in Python.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/liamdoult/',
    author='Liam Doult',
    author_email='liam.doult@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='CI integration testing',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.5, <4',
    install_requires=[
        'docker',
    ],
    extras_require={
        'dev': ['check-manifest'],
        'test': [
            'pymongo',
            'pika',
            'redis',
        ],
    },
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/LiamDoult/python-template/issues',
        'Source': 'https://github.com/LiamDoult/python-template/',
    },
)
