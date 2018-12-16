#!/usr/bin/env python
from setuptools import setup, find_packages
DEPENDENCIES = [
    "PyYAML",
    "Flask",
    "mysql-connector",
]

setup(name="gfui",
      version=0.09,
      description="GoFlow basic user interface",
      author="Adam Baumeister",
      author_email="adam.baumeister@csiro.au",
      packages=find_packages(),
      install_requires=DEPENDENCIES,
      scripts=['start.py'],
      include_package_data=True,
      )

