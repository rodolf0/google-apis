#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
  name = "google-apis",
  version = "0.1",
  packages = find_packages(),

  install_requires = ['google-api-python-client', 'httplib2'],

  include_package_data = True,

  entry_points={
    'console_scripts': [
      'agenda = gcalendar.agenda:main'
    ]
  },

  author = "rodolfo granata",
  author_email = "warlock.cc@gmail.com",
  description = "google api tests",
)

# vim: set sw=2 sts=2 : #
