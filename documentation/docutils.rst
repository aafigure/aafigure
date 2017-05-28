==========
 Docutils
==========

The docutils directive is provided in `aafigure/docutils`.


Docutils directive
==================
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


Docutils plug-in
================
The docutils-aafigure_ extension depends on the aafigure package also requires
``setuptools`` (often packaged as ``python-setuptools``) and Docutils_ itself
(0.5 or newer) must be installed.

After that, the ``aafigure`` directive will be available.

.. _docutils-aafigure: http://pypi.python.org/pypi/aafigure
.. _Docutils: http://docutils.sf.net


