try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

config = {
	'description': 'Toy language with compiler for SPIM written in Python 3',
	'author': 'Mark Provan',
	'url': None,
	'download_url': None,
	'author_email': 'markprovanp@gmail.com'
	'version': '0.1'
	'install_requires': ['nose'],
	'packages': ['noggin'],
	'scripts': [],
	'name' 'noggin'
}