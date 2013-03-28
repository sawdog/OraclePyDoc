#!python
"""setup file, used to install the orapydoc package.

   This package consists of tools to generate documentation of
   oracle schemas

   Scripts::

     orapydoc

"""
from setuptools import setup, find_packages
import sys
VERSION = open('version.txt').read().strip()

scripts = []

setup(name='orapydoc',
      version=VERSION,
      description='utility to generate rst documentation of oracle schemas',
      author='Andrew Sawyers',
      author_email='andrew.sawyers@dnr.wa.gov',
      license='BSD',
      long_description = open('README.txt').read(),
      keywords = 'utilities oracle documentation reST structured text',
      url = 'http://svn/viewvc/datamart/projects/oraclePyDoc/trunk',
      packages = find_packages(),
      py_modules = [],
      zip_safe = False,
      entry_points = {'console_scripts': [
             'orapydoc = runner:main',]},
      classifiers = [f.strip() for f in """
      Development Status :: 3 - Alpha
      Intended Audience :: Developers
      License :: OSI Approved :: BSD
      Operating System :: OS Independent
      Programming Language :: Python
      Topic :: Software Development :: Libraries :: Python Modules
      Topic :: System :: System Administration
      Topic :: Utilities""".splitlines() if f.strip()],
      scripts = scripts,
      install_requires = [],
)
