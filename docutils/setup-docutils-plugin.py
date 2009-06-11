# $Id$
# Author: Lea Wiemann <LeWiemann@gmail.com>
# Author: Chris Liechti <cliechti@gmx.net>
# Copyright: This file has been placed in the public domain.

from setuptools import setup, find_packages
setup(
    name = 'docutils-aafigure',
    version = '0.3',
    description = "ASCII art figures for reStructuredText",
    long_description = """\
This package provides a docutils directive that allows to integrate ASCII art
figures directly into the text.

reST example::

    .. aafigure::

            +-----+   ^
            |     |   |
        --->+     +---o--->
            |     |   |
            +-----+   V

Please see README.txt for examples.

requires docutils (>= 0.5).

""",
    author = 'Chris Liechti',
    author_email = 'cliechti@gmx.net',
    install_requires = ['aafigure>=0.2', 'docutils>=0.5'],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    platforms = 'any',
    py_modules = [ 'aafigure_directive'],
    entry_points = {
        'docutils.parsers.rst.directives': [
            'aafigure = aafigure_directive:AAFigureDirective'
        ],
    },

)
