==================
 MoinMoin plug-in
==================
MoinMoin_ is a popular Wiki engine. The plug-in allows to use aafigure drawings
within wiki pages.

Copy the file ``aafig.py`` from ``examples/moinmoin`` to
``wiki/data/plugin/parser`` of the wiki. The aafigure module itself needs to
be installed for the Python version that is used to run MoinMoin_ (see above for
instructions).

Tested with MoinMoin 1.8.

See also: http://moinmo.in/ParserMarket/AaFigure

.. _MoinMoin: http://moinmo.in

Usage
=====
ASCII Art figures can be inserted into a MoinMoin_ WikiText page the following
way::

    {{{#!aafig scale=1.5 foreground=#ff1010
    DD o--->
    }}}

The parser name is ``aafig`` and options are appended, separated with spaces.
Options that require a value take that after a ``=`` without any whitespace
between option and value.  Supported options are:

    - ``scale=<float>``
    - ``aspect=<float>``
    - ``textual``
    - ``textual_strict``
    - ``proportional``
    - ``linewidth=<float>``
    - ``foreground=#rrggbb``
    - ``fill=#rrggbb``

There is no ``background`` as the SVG backend ignores that. And it is not possible
to pass generic options.

The images are generated and stored in MoinMoin's internal cache. So there is
no mess with attached files on the page. Each change on an image generates a
new cache entry so the cache may grow over time. However the files can be
deleted with no problem as they can be rebuilt when the page is viewed again
(the old files are not automatically deleted as they are still used when older
revision of a page is displayed).
