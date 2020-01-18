#!/usr/bin/env python
from setuptools import setup, find_packages
import re
import os


def get_version():
  fn = os.path.join(os.path.dirname(__file__), "scrapy_camouflage", "__init__.py")
  with open(fn) as f:
    return re.findall("__version__ = '([\d.\w]+)'", f.read())[0]

def get_long_description():
  with open('README.md') as fh:
    return fh.read()

setup(
  name='scrapy-camouflage',
  version=get_version(),
  author='Tianhui Li',
  license='Apache License',
  long_description=get_long_description(),
  description="Rotating proxies and user agents for Scrapy",
  url='https://github.com/tianhuil/scrapy-camouflage',
  packages=find_packages(exclude=['tests']),
  classifiers=[
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: Apache License',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'Framework :: Scrapy',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
  ],
)
