# encoding: utf-8
from setuptools import setup
from plugnplay import __version__

setup(
  name="plugnplay",
  version=__version__,
  url="http://github.com/daltonmatos/plugnplay",
  license="GPLv2",
  description="A Generic plug-in system for python",
  author="Dalton Barreto",
  author_email="daltonmatos@gmail.com",
  long_description=open('README.rst').read(),
  packages=['plugnplay'],
  classifiers=[
    "License :: OSI Approved :: GNU General Public License (GPL)",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Topic :: Software Development :: Libraries :: Application Frameworks"
    ])
