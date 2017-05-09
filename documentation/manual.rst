========
 Manual
========

Overview
========

The original idea was to parse ASCII art images, embedded in reST documents and
output an image. This would mean that simple illustrations could be embedded as
ASCII art in the reST source and still look nice when converted to e.g. HTML.

aafigure can be used to write documents that contain drawings in plain text
documents and these drawings are converted to appropriate formats for e.g. HTML
or PDF versions of the same document.

Since then aafigure also grew into a standalone application providing a command
line tool for ASCII art to image conversion.


ASCII Art
---------
The term "ASCII Art" describes a `wide field`_.

* (small) drawings found in email signatures
* smilies :-)
* raster images (this was popular to print images on text only printers a *few*
  years ago)
* simple diagrams using lines, rectangles, arrows

aafigure aims to parse the last type of diagrams.

.. _`wide field`: http://en.wikipedia.org/wiki/ASCII_art


Other text to image tools
-------------------------
There are of course also a lot of other tools doing text to image conversions
of some sort. One of the main differences is typically that other tools use a
description language to generate images from rules. This is a major difference
to aafigure which aims to convert good looking diagrams/images etc. in text
files to better looking images as bitmap or vector graphics. Here are some
examples (by no means a complete list):

Graphviz_
    Graphviz is a very popular tool that is excellent for displaying graphs and
    networks. It does this by reading a list of relations between nodes and it
    automatically finds the best way to place all the nodes in a visually
    appealing way.

    This is quite different from aafigure and both have their strengths.
    Graphviz is very well suited to document state machines, class hierarchies
    and other graphs.

Mscgen_
    A tool that is specialized for sequence diagrams (used to describe
    software, UML).

ditaa_
    Convert diagrams to images.

.. _Graphviz: http://www.graphviz.org/
.. _mscgen: http://www.mcternan.me.uk/mscgen/
.. _ditaa: http://ditaa.sourceforge.net/


Installation
============

aafigure
--------
::

    pip install aafigure

This installs a package that can be used from python (``import aafigure``) and
a command line script called ``aafigure``.

The Python Imaging Library (PIL) needs to be installed when support for bitmap
formats is desired and it will need ReportLab for PDF output.

Requirements
~~~~~~~~~~~~

* reportlab_ (for LaTeX/PDF output)
* PIL_ or Pillow_ (for any image format other than SVG or PDF)

.. _reportlab: http://www.reportlab.org/
.. _PIL: http://www.pythonware.com/products/pil/
.. _Pillow: https://python-pillow.org/


Usage
=====
Command line tool
-----------------
::

    aafigure test.txt -t png -o test.png

The tool can also read from standard in and supports many options. Please look
at the command's help (or man page)::

    aafigure --help

