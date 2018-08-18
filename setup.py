#!/usr/bin/env python

from setuptools import find_packages, setup

setup(
    name='Xagon',
    version='0.1',
    description='A pyxel based game.',
    author='Fabien Dupont',
    author_email='fabien.dupont@fullsave.com',
    packages=find_packages(exclude=["tests.*", "tests"]),
    entry_points={
        'console_scripts': ['Xagon=Xagon.shell:main'],
    },
    include_package_data=True,
    data_files=[
        ('assets', ['Xagon/assets/logo.png'])
    ],
    install_requires=[
        'pyxel',
        ],
    )
