#!/usr/bin/python3
from setuptools import setup, find_packages

setup(
    name='kraken2_2otu',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'pandas',
        'numpy',
        'ete3',
    ],
    entry_points='''
        [console_scripts]
        kraken2_2otu=kraken2_2otu.cli:read_data
    ''',
)