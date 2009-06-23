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


Other text to image tools
-------------------------
There are of course also a lot of other tools doing text to image conversions
of some sort. One of the main differences is typically that other tools use a
description language to generate images from rules. This is a major difference
to aafigure which aims to convert good looking diagrams/images etc in text
files to better looking images.

Graphviz
~~~~~~~~
Graphviz is a very popular tool that is excellent for displaying graphs and
networks. It does this by reading a list of relations between nodes and it
automatically finds the best way to place all the nodes in a visually appealing
way.

This is quite different from aafigure and both have their strengths. Graphviz
is very well suited to document state machines, class hierarchies and other
graphs.


Usage
-----
Command line tool
~~~~~~~~~~~~~~~~~
::

    aafigure test.txt -t png -o test.png

The tool can also read from standard in and supports many options. Please look
at the command's help (or man page)::

    aafigure --help

Within Docutils
~~~~~~~~~~~~~~~
A ``:aafigure:`` directive is provided that allows to insert images.

::

    ./rst2html.py README.txt >README.html

This results in the ``README.html`` file and a ``.svg`` fiel (or the specified
file type) for each ``:aafigure:``.

The resulting ``README.html`` file can be viewed a SVG capable browser. It has
been tested with Firefox 1.5, 2.0 and 3.0.

Within Sphinx
~~~~~~~~~~~~~
In ``conf.py`` add::

    extensions = ['sphinxcontrib.aafig']

Diagrams can now be inserted with a ``:aafig:`` directive. The output format is
automatically chosen depending on the generated document format (e.h. HTML or
PDF).


Installation
============

aafigure
--------
To install aafigure, you need to have administrator rights on your system (be
root). Type ``python setup.py install`` to install aafigure.

This installs a package that can be used from python (``import aafigure``) and
a command line script called ``aafigure``.

The Python Imaging Library (PIL) needs to be installed when support for bitmap
formats is desired and it will need ReportLab for PDF output.

Alternatively it can be installed from PyPy, either manually downloading the
files and installing as described above or using::

    easy_install -U aafigure

There are also packaged versions for:
* Ubuntu (https://launchpad.net/~aafigure-team/+archive/ppa)
* Arch Linux ("aafigure" or "aafigure-bzr" in category "unsupported")


Docutils plugin
---------------
The docutils-aafigure extension depends on the aafigure package also requires
``setuptools`` (often packaged as ``python-setuptools``) and docutils itself
(0.5 or newer) must be installed.

After that, the ``aafigure`` directive will be available.

Sphinx plugin
-------------
sphinxcontrib-aafig_ is a plugin similar to the Docutils plugin, but it
automatically selects the image format depending on the output format.

XXX elaborate

.. _sphinxcontrib-aafig: http://pypi.python.org/pypi/sphinxcontrib-aafig


Short introduction
==================
In a Sphinx document an image can be inserted like this::

    .. aafig::

        -->

Which results in an image like this:

.. aafig::

    -->

The same contents could also have been placed in a file and then be converted
with the aafigure command line tool.

Docutils directive
------------------
The ``aafigure`` directive has the following options:

- ``:scale: <float>``   enlarge or shrink image

- ``:line_width: <float>``   change line with (svg only currently)

- ``:format: <str>`` choose backend/output format: 'svg', 'png', all
  bitmap formats that PIL supports can be used but only few make sense. Line
  drawings have a good compression and better quality when saved as PNG
  rather than a JPEG. The best quality will be achieved with SVG, tough not
  all browsers support this vector image format at this time.

- ``:foreground: <str>``   foreground color in the form ``#rgb`` or ``#rrggbb``

- ``:background: <str>``   background color in the form ``#rgb`` or ``#rrggbb``
  (*not* for SVG output)

- ``:fill: <str>``   fill color in the form ``#rgb`` or ``#rrggbb``

- ``:name: <str>``   use this as filename instead of the automatic generated
  name

- ``:aspect: <float>``  change aspect ratio. Effectively it is the width of the
  image that is multiplied by this factor. The default setting ``1`` is useful
  when shapes must have the same look when drawn horizontally or vertically.
  However, ``:aspect: 0.5`` looks more like the original ASCII and even smaller
  factors may be useful for timing diagrams and such. But there is a risk that
  text is cropped or is draw over an object beside it.

  The stretching is done before drawing arrows or circles, so that they are
  still good looking.

- ``:proportional: <flag>``  use a proportional font instead of a mono-spaced
  one.


Sphinx directive
----------------
It is called ``aafig``. The same options as for the docutils directive apply
with the exception of ``format``. That option is not supported as the format
is automatically determined.


Lines
-----
The ``-`` and ``|`` are normally used for lines. ``_`` and ``~`` can also be
used. They are slightly longer lines than the ``-``. ``_`` is drawn a bit
lower and ``~`` a bit upper. ``=`` gives a thicker line. The later three line
types can only be drawn horizontally.
::

  ---- |         ___  ~~~|
       | --  ___|        |    ===
                         ~~~

.. aafig::

  ---- |         ___  ~~~|
       | --  ___|        |    ===
                         ~~~

It is also possible to draw diagonal lines. Their use is somewhat restricted
tough. Not all cases work as expected.

.. aafig::

                                     +
      |  -  +   |  -  +   |  -  +   /               -
     /  /  /   /  /  /   /  /  /   /     --     |/| /    +
    |  |  |   +  +  +   -  -  -   /     /  \        -   \|/  |\
                                 +     +    +          +-+-+ | +
    |  |  |   +  +  +   -  -  -   \     \  /        -   /|\  |/
     \  \  \   \  \  \   \  \  \   \     --     |\| \    +
      |  -  +   |  -  +   |  -  +   \               -
                                     +

And drawing longer diagonal lines with different angles looks ugly...

.. aafig::

    +      |
     \    /
      \  /
       --


Arrows
------
Arrow styles are::

    --->   | | | | | |
    ---<   | | | | | |
    ---o   ^ V v o O #
    ---O
    ---#

.. aafig::

    --->   | | | | | |
    ---<   | | | | | |
    ---o   ^ V v o O #
    ---O
    ---#

Boxes
-----
Boxes are automatically draw when the edges are made with ``+``, filled
boxes are made with ``X`` (must be at least two units high or wide).
It is also possible to make rounded edges in two ways::

    +-----+   XXX  /--\     --   |
    |     |   XXX  |  |    /    /
    +-----+   XXX  \--/   |   --

.. aafig::

    +-----+   XXX  /--\     --   |
    |     |   XXX  |  |    /    /
    +-----+   XXX  \--/   |   --

Fills
-----

Upper case characters generate shapes with borders, lower case without border.
Fills must be at least two characters wide or high. (This reduces the chance
that it is detected as Fill instead of a string)

.. aafig::

    A   B   C   D   E   F   G   H   I   J   K   L   M
     AA  BB  CC  DD  EE  FF  GG  HH  II  JJ  KK  LL  MM
     AA  BB  CC  DD  EE  FF  GG  HH  II  JJ  KK  LL  MM

     aa  bb  cc  dd  ee  ff  gg  hh  ii  jj  kk  ll  mm
     aa  bb  cc  dd  ee  ff  gg  hh  ii  jj  kk  ll  mm

    N   O   P   Q   R   S   T   U   V   W   X   Y   Z
     NN  OO  PP  QQ  RR  SS  TT  UU  VV  WW  XX  YY  ZZ
     NN  OO  PP  QQ  RR  SS  TT  UU  VV  WW  XX  YY  ZZ

     nn  oo  pp  qq  rr  ss  tt  uu  vv  ww  xx  yy  zz
     nn  oo  pp  qq  rr  ss  tt  uu  vv  ww  xx  yy  zz

Complex shapes can be filled:

.. aafig::

    CCCCC     C         dededede
     C  CCCC  CC        dededede
     CC    CCCCC        dededede

Text
----
The images may contain text too. There are different styles to enter text:

*direct*

By default are repeated characters detected as fill::

    Hello World  dd d
                    d

.. aafig::

    Hello World  dd d
                    d

*quoted*

Text between quotes has priority over any graphical meaning::

    "Hello World"  dd d
                      d

.. aafig::

    "Hello World"  dd d
                      d

``"``, ``'`` and ``\``` are all valid quotation marks. The quotes are not
visible in the resulting image. This not only disables fills (see below), it
also treats ``-``, ``|`` etc. as text.

*textual option*

The ``:textual:`` option disables horizontal fill detection. Fills are only
detected when they are vertically at least 2 characters high::

    Hello World  dd d
                    d

.. aafig::
    :textual:

    Hello World  dd d
                    d


Other
-----

::

    * { }

.. aafig::

    * { }

