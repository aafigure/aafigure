========
 Sphinx
========

This extension adds the ``aafig`` directive that automatically selects the
image format to use according to the Sphinx_ writer used to generate the
documentation.


Quick Example
-------------

This source::

    .. aafig::
        :aspect: 60
        :scale: 150
        :proportional:
        :textual:

        +-------+         +-----------+
        | Hello +-------->+ aafigure! |
        +-------+         +-----------+

is rendered as:

.. aafig::
    :aspect: 60
    :scale: 150
    :proportional:
    :textual:

    +-------+         +-----------+
    | Hello +-------->+ aafigure! |
    +-------+         +-----------+


Enabling the extension in Sphinx_
---------------------------------

Just add ``aafigure.sphinxext`` to the list of extensions in the ``conf.py``
file. For example::

    extensions = ['aafigure.sphinxext']


Options
=======
The ``aafig`` directive has the following options:

- ``:scale: <int>``   enlarge or shrink image

- ``:line_width: <float>``   change line with (SVG only currently)

- ``:foreground: <str>``   foreground color in the form ``#rgb`` or ``#rrggbb``

- ``:background: <str>``   background color in the form ``#rgb`` or ``#rrggbb``
  (*not* for SVG output)

- ``:fill: <str>``   fill color in the form ``#rgb`` or ``#rrggbb``

- ``:aspect: <int>``  change aspect ratio. Effectively it is the width of the
  image that is multiplied by this percentage. The default setting ``1`` is useful
  when shapes must have the same look when drawn horizontally or vertically.
  However, ``:aspect: 50`` looks more like the original ASCII and even smaller
  factors may be useful for timing diagrams and such. But there is a risk that
  text is cropped or is draw over an object besides it.

  The stretching is done before drawing arrows or circles, so that they are
  still good looking.

- ``:proportional:``  use a proportional font instead of a mono-spaced

- ``:textual:``  prefer to detect text instead of fills

- ``:rounded:``  use arcs instead of straight lines for many diagonals

- ``:scale:`` and ``:aspect:`` options are specified using percentages
  (without the *%* sign), to match the reStructuredText_ image directive.


Configuration
-------------

A few configuration options are added (all optional, of course ;) to Sphinx_
so you can set them in the ``conf.py`` file:

``aafig_format`` <dict>:
   image format used for the different builders. All ``latex``, ``html`` and
   ``text`` builder are supported, and it should be trivial to add support for
   other builders if they correctly handle images (and if aafigure can render
   an image format suitable for that builder) by just adding the correct format
   mapping here.

   A special format ``None`` is supported, which means not to use aafigure to
   render the image, just show the raw ASCII art as is in the resulting
   document (using a literal block). This is almost only useful for the text
   builder.

   You can specify the format - builder mapping using a dict. For example::

      aafig_format = dict(latex='pdf', html='svg', text=None)

   These are the actual defaults.

``aafig_default_options`` <dict>:
    default aafigure options. These options are used by default unless they
    are overridden explicitly in the ``aafig`` directive. The default aafigure
    options are used if this is not specified. You can provide partial
    defaults, for example::

        aafig_default_options = dict(scale=150, aspect=50, proportional=True)

    Note that in this case the ``aspec`` and ``scale`` options are specified
    as floats, as originally done by aafigure.


TODO
====

* Add color validation for ``fill``, ``background`` and ``foreground`` options.
* Add ``aa`` role for easily embed small images (like arrows).


.. Links:
.. _reStructuredText: http://docutils.sourceforge.net/rst.html
.. _Sphinx: http://sphinx-doc.org/


History
=======
This extension was once shipped separately: `sphinxcontrib-aafig website`__.

__ http://packages.python.org/sphinxcontrib-aafig/

