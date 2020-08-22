import setuptools

with open('README.md') as f:
	long_description = f.read()

setuptools.setup(
	name = 'pool_workers',
	version = '0.0.2',
	author='Mohammed ER-Ramouchy',
	author_email='mohammed@ramouchy.com',
	description='A small package for dealing with pools, workers and queues.',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/medram/pool_workers',
	packages=setuptools.find_packages(),
	classifiers=[
		'Programming Language :: Python :: 3.6',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent'
	],
	python_requires='>=3.6'
)