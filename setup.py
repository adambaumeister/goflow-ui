#!/usr/bin/env python
from setuptools import setup, find_packages
DEPENDENCIES = [
    "PyYAML",
    "Flask",
    "mysql-connector",
]

setup(name="goflow-ui",
      version=0.06,
      description="GoFlow basic user interface",
      author="Adam Baumeister",
      author_email="adam.baumeister@csiro.au",
      packages=find_packages(),
      install_requires=DEPENDENCIES,
      scripts=['main.py'],
      include_package_data=True,
      package_data={'': ['templates/*', 'static/*']},
      )

