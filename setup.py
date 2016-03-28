from setuptools import setup

setup(
	name='equitext',
	version='1',
	py_modules=['equitext'],
	test_suite='tests',

	author='foobuzz',
	author_email='dprosium@gmail.com',
	description='A text-to-text encoding. Characters have the same number of '
	'occurences in the encoded text',
	keywords='encoding text character occurence frequency',
	url='https://github.com/foobuzz/equitext'
)