==========
 Appendix
==========

Implementation
==============

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
====

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



