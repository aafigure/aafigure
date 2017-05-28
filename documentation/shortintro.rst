====================
 Short introduction
====================

Lines
=====
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
though. Not all cases work as expected.

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

With ``rounded`` flag:

.. aafig::
    :rounded:

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

.. aafig::
    :rounded:

    +      |
     \    /
      \  /
       --


Arrows
======
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
=====
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
=====

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
====
The images may contain text too. There are different styles to enter text:

direct
------

By default are repeated characters detected as fill::

    Hello World  dd d
                    d

.. aafig::

    Hello World  dd d
                    d

quoted
------

Text between quotes has priority over any graphical meaning::

    "Hello World"  dd d
                      d

.. aafig::

    "Hello World"  dd d
                      d

``"``, ``'`` and ``\``` are all valid quotation marks. The quotes are not
visible in the resulting image. This not only disables fills (see below), it
also treats ``-``, ``|`` etc. as text.

textual option
--------------

The ``:textual:`` option disables horizontal fill detection. Fills are only
detected when they are vertically at least 2 characters high::

    Hello World  dd d
                    d

.. aafig::
    :textual:

    Hello World  dd d
                    d


Other
=====

::

    * { }

.. aafig::

    * { }

