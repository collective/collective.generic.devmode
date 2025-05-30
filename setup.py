import os, sys

from setuptools import setup, find_packages


def read(*rnames):
    return open(
        os.path.join('.', *rnames)
    ).read()

long_description = "\n\n".join(
    [read('README.rst'),
     read('docs', 'INSTALL.txt'),
     read('docs', 'HISTORY.txt'),
    ]
)

classifiers = [
    "Programming Language :: Python",
    "Topic :: Software Development",]

name = 'collective.generic.devmode'
version = '1.0'
setup(
    name=name,
    namespace_packages=['collective',                'collective.generic', 'collective.generic.devmode',],
    version=version,
    description='Sanitize a plone site for development use by Makina Corpus.',
    long_description=long_description,
    classifiers=classifiers,
    keywords='',
    author='MakinaCorpus',
    author_email='freesoftware@makina-corpus.com',
    url='http://pypi.python.org/pypi/%s' % name,
    license='GPL',
    packages=find_packages('src'),
    package_dir = {'': 'src'},
    include_package_data=True,
    extras_require = {
        'test': ['ipython', 'zope.testing']
    },
    install_requires=[
        'setuptools',
        # -*- Extra requirements: -*-
    ],
    # define there your console scripts
    entry_points = {
        'console_scripts': [
            'cg.devmode = collective.generic.devmode.devmode:main',
        ],
    }

)
# vim:set ft=python:
