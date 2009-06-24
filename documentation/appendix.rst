==========
 Appendix
==========

API and Implementation Notes
============================

External Interface
------------------
Most users of the module will use one of the following two functions. They
provide a high level interface. They are also directly accessible as
``aafigure.process`` respectively ``aafigure.render``.

.. module:: aafigure.aafigure

.. autofunction:: aafigure.aafigure.process
.. autofunction:: aafigure.aafigure.render

The command line functionality is implemented in the ``main`` function.

.. autofunction:: aafigure.aafigure.main


Internal Interface
------------------
The core functionality is implemented in the following class.

.. autoclass:: aafigure.aafigure.AsciiArtImage
    :members: __init__, recognize

Images are built using the following shapes. Visitor classes must be able to
process these types.

.. automodule:: aafigure.shapes
    :members:


Options
-------
The ``options`` dictionary is used in a number of places.
Valid keys (and their defaults) are:

Defining the output:

    ``file_like`` <str>:
        use the given file like object to write the output. The object
        needs to support a ``.write(data)`` method.

    ``format`` <str>:
        choose backend/output format: 'svg', 'pdf', 'png' and all bitmap
        formats that PIL supports can be used but only few make sense. Line
        drawings have a good compression and better quality when saved as
        PNG rather than a JPEG. The best quality will be achieved with SVG,
        tough not all browsers support this vector image format at this
        time (default: ``'svg'``).

Options influencing how an image is parsed:

    ``textual`` <bool>:
        disables horizontal fill detection. Fills are only detected when
        they are vertically at least 2 characters high (default: ``False``).

    ``proportional`` <bool>:
        use a proportional font. Proportional fonts are general better
        looking than monospace fonts but they can mess the figure if you
        need them to look as similar as possible to the ASCII art (default:
        ``False``).

Visual properties:

    ``background`` <str>:
        background color in the form ``#rgb`` or ``#rrggbb``, *not* for SVG
        output (default: ``#000000``).

    ``foreground`` <str>:
        foreground color in the form ``#rgb`` or ``#rrggbb`` (default:
        ``#ffffff``).

    ``fill`` <str>:
        fill color in the form ``#rgb`` or ``#rrggbb`` (default: same as
        ``foreground`` color).

    ``line_width`` <float>:
        change line with, SVG only currently (default: ``2.0``).

    ``scale`` <float>:
        enlarge or shrink image (default: ``1.0``).

    ``aspect`` <float>:
        change aspect ratio. Effectively it is the width of the image that
        is multiplied by this factor. The default setting ``1`` is useful
        when shapes must have the same look when drawn horizontally or
        vertically.  However, 0.5 looks more like the original ASCII and
        even smaller factors may be useful for timing diagrams and such.
        But there is a risk that text is cropped or is drawn over an object
        besides it.

        The stretching is done before drawing arrows or circles, so that
        they are still good looking (default: ``1.0``).

Miscellaneous options:

    ``debug`` <bool>:
        for now, it only prints the original ASCII art figure text
        (default: ``False``).

Visitors
--------
A visitor that can be used to render the image must provide the following
function (it is called by :func:`process`)

.. currentmodule:: your

.. class:: Visitor

    .. method:: visit_image(aa_image)

        An :class:`AsciiArtImage` instance is passed as parameter. The visiting
        function needs to implement a loop processing the ``shapes`` attribute.

        This function must take care of actually outputting the resulting image
        or it must provide the data in a form useful for the caller
        (:func:`process` returns the visitor so that the result can be read for
        example).

Example stub class:

.. code-block:: python

    class Visitor:
        def visit_image(self, aa_image):
            self.visit_shapes(aa_image.shapes)

        def visit_shapes(self, shapes):
            for shape in shapes:
                shape_name = shape.__class__.__name__.lower()
                visitor_name = 'visit_%s' % shape_name
                if hasattr(self, visitor_name):
                    getattr(self, visitor_name)(shape)
                else:
                    sys.stderr.write("WARNING: don't know how to handle shape %r\n"
                        % shape)

        def visit_group(self, group):
            self.visit_shapes(group.shapes)

        # for actual output implement visitors for all the classes in
        # aafigure.shapes:

        def visit_line(self, lineobj):
            ...
        def visit_circle(self, circleobj):
            ...
        etc...

Source tree
-----------
The sources can be checked out using bazaar_::

    bzr lp:aafigure

.. _bazaar: http://bazaar-vcs.org


Files in the ``aafigure`` package:

``aafigure.py``
    ASCII art parser. This is the main module.

``shapes.py``
    Defines a class hierachy for geometric shapes such as lines, circles etc.

``error.py``
    Define common exception classes.

``aa.py``
    ASCII art output backend. Intended for tests, not really useful for the end
    user.

``pdf.py``
    PDF output backend. Depends on reportlab.

``pil.py``
    Bitmap output backend. Using PIL, it can write PNG, JPEG and more formats.

``svg.py``
    SVG output backend.


Files in the ``docutils`` directory:

``aafigure_directive.py``
    Implements the ``aafigure`` Docutils directive that takes these
    ASCII art figures and generates a drawing.

The ``aafigure`` module contains code to parse ASCII art figures and create
a list of of shapes. The different output modules can walk through a list of
shapes and write image files.


TODO
----

- Symbol detection: scan for predefined shapes in the ASCII image
  and output them as symbol from a library

- Symbol libraries for UML, flowchart, electronic schematics, ...

- The way the image is embedded is a hack (inserting a tag trough a raw node...)

- Search for ways to bring in color. Ideas:

    - have an :option: to set color tags. Shapes that touch such a tag
      inherit it's color. The tag would be visible in the ASCII source tough::

        .. aafig::
            :colortag: 1:red, 2:blue

            1--->  --->2

    - ``:color: x,y,color`` but counting coordinates is no so fun

    drawback: both are complex to implement, searching for shapes that belong
    together. It's also not always wanted that e.g. when a line touches a
    box, both have the same color

- aafigure probably needs arguments like ``font-family``, ...

- Punctuation not included in strings (now a bit improved but if it has a
  graphical meaning , then that is chooses, even if it makes no sense),
  underlines in strings are tricky to detect...

- Dotted lines? ``...``
  e.g. for ``---...---`` insert a dashed line instead of 3 textual dots.
  Vertical dashed lines should also work with ``:``.

- Group shapes that belong to an object, so that it's easier to import and
  change the graphics in a vector drawing program. [partly done]

- Path optimizer, it happens that many small lines are output where a long
  line could be used.


Authors and Contact
===================

- Chris Liechti: original author
- Leandro Lucarella: provided many patches

The project page is at https://launchpad.net/aafigure
It should be used to report bugs and feature requests.


License
=======
Copyright (c) 2006-2009 aafigure-team
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright
  notice, this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright
  notice, this list of conditions and the following disclaimer in the
  documentation and/or other materials provided with the distribution.
* Neither the name of the aafigure-team nor the
  names of its contributors may be used to endorse or promote products
  derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE AAFIGURE-TEAM ''AS IS'' AND ANY
EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE AAFIGURE-TEAM BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.



