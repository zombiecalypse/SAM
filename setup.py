#!/usr/bin/python

from setuptools import setup
from main import version

setup(
		name = 'Space Alert Mission Generator',
		version = version,
		description = 'Generating random missions for the Space Alert game.',
		author = 'Aaron Karper',
		author_email = 'maergil@gmail.com',
		packages = ['Python-Logger/PyLogger'],
		install_requires = [
			'setuptools'])
