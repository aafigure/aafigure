===================
 AAFIGURE EXAMPLES
===================

This directory contains a few example input files for the aafigure tool. It
also has an example on how to use the module within your own Python programs.


Using the ``.txt`` files
========================
The text files can be converted with aafigure, for example::

    aafigure fill.txt -o fill.svg

aafigure as library
===================
``demo.py`` is a short example on how the module can be used from other Python
programs. The MoinMoin plug-in is of course an other example showing this.

MoinMoin plug-in
================
The ``moinmoin`` directory contains a Parser plug-in for the MoinMoin wiki.
More information can be found in the manual. Hint: copy the file to
``wiki/data/plugin/parser`` and it's ``{{{#!aafig ...``.
