==========
 Examples
==========

Simple tests
------------
Different arrow types:

.. aafig::

    <-->  >->   --> <--
    >--<  o-->  -->+<--
    o--o          o=>

Boxes and shapes:

.. aafig::

    +---------------+
    |A box with text|
    +---------------+

.. aafig::

        ---> | ^|   |   +++
        <--- | || --+-- +++
        <--> | |V   |   +++<-
     __             __    ^
    |  |__  +---+  |__|   |
            |box|   ..
            +---+  Xenophon


Flow chart
----------
.. aafig::
    :textual:

        /---------\
        |  Start  |
        \----+----/
             |
             V
        +----+----+
        |  Init   |
        +----+----+
             |
             +<-----------+
             |            |
             V            |
        +----+----+       |
        | Process |       |
        +----+----+       |
             |            |
             V            |
        +----+----+  yes  |
        |  more?  +-------+
        +----+----+
             | no
             V
        /----+----\
        |   End   |
        \---------/


UML
---
No not really, yet. But you get the idea.

.. aafig::
    :scale: 0.8

    +---------+  +---------+  +---------+
    |Object 1 |  |Object 2 |  |Object 3 |
    +----+----+  +----+----+  +----+----+
         |            |            |
         |            |            |
         X            |            |
         X----------->X            |
         X            X            |
         X<-----------X            |
         X            |            |
         X            |            |
         X------------------------>X
         |            |            X
         X----------->X            X---+
         X            X            X   |
         |            |            X<--+
         X<------------------------X
         X            |            |
         |            |            |
         |            |            |

.. aafig::
    :scale: 0.8

    +---------+         +---------+     +---------+
    |  Shape  |         |  Line   |     |  Point  |
    +---------+         +---------+   2 +---------+
    | draw    +<--------+ start   +----O+ x       |
    | move    +<-+      | end     |     | y       |
    +---------+   \     +---------+     +---------+
                   \
                    \   +---------+
                     +--+ Circle  |
                        +---------+
                        | center  |
                        | radius  |
                        +---------+

.. aafig::

                             /-----------\     yes /----------\
                          -->| then this |--->*--->| and this |
                      +  /   \-----------/    |no  \----------/
     /------------\   +--                     |
     | First this |-->+                       |
     \------------/   +--                     |
                      +  \   /---------\      V        /------\
                          -->| or that |----->*------->| Done |
                             \---------/               \------/

Electronics
-----------
It would be cool if it could display simple schematics.

.. aafig::
    :fill: #fff

          Iin +-----+      Iout
        O->---+ R1  +---o-->-----O
       |      +-----+   |         |
    Vin|       100k   ----- C1    | Vout
       |              ----- 100n  |
       v                |         v
        O---------------o--------O

.. - Resistor should not be filled -> can be solved by symbol detection

- Capacitor not good, would prefer ``--||--``  -> symbol detection


.. aafig::

       |/|       |\|       | |     +---+       e|
    ---+ +---  --+ +--   --+ +--  -+   +-    b|/
       |\|       |/|       | |     +---+    --+
                                              |\
       |        |           |        |         c|
      -+-      -+-         -+-      +++
      / \      \ /                  | |    -   -
      -+-      -+-         -+-      | |    c\ /e
       |        |           |       +++     -+-
                                     |       |b

- Diodes OK

- Caps not optimal. Too far apart in image, not very good recognisable in
  ASCII. Space cannot be removed as the two ``+`` signs would be connected
  otherwise. The schematic below uses an other style.

- Arrows in transistor symbols can not be drawn

Here is a complete circuit with different parts:

.. aafig::
    :fill: #fff
    :scale: 0.8
    :textual:

                         Q1  _  8MHz
                           || ||
                      +----+| |+----+
                      |    ||_||    |
                      |             |
                +-----+-------------+-----+
                |    XIN           XOUT   |
                |                         |
                |                    P3.3 +--------------+
    SDA/I2C O---+ P2.0                    |              |
                |                         |             e|
                |        MSP430F123       |   +----+  b|/  V1
    SCL/I2C O---+ P2.1               P3.4 +---+ R1 +---+   PNP
                |                         |   +----+   |\
                |           IC1           |      1k     c|    +----+
                |                         |              o----+ R3 +---O TXD/RS232
                |    VCC             GND  |              |    +----+
                +-----+---------------+---+              |      1k
                      |               |                  |    +----+
                      |               |                  +----+ R2 +---O RXD/RS232
                      |               |                       +----+
                      |               |                         10k
    GND/I2C O---o-----+----o----------o-----------o--------------------O GND/RS232
                |     |    |   C1     |           |   C2
               =+=    |  ----- 1u     |         ----- 10u
                      |  ----- 5V +---+---+     ----- 16V
                      |    |      |  GND  |       |            D1|/|
                      +----o------+out  in+-------o----------o---+ +---O RTS/RS232
                                  |  3V   |                  |   |\|
                                  +-------+                  |
                                   IC2                       | D2|/|
                                                             +---+ +---O DTR/RS232
                                                                 |\|


Timing diagrams
---------------
.. aafig::
    :aspect: 0.5

      ^    ___     ___           ____
    A |___|   |___|   |_________|    |______
      |      ___        ___           __
    B |_____|   |______|   |________XX  XX__
      |
      +-------------------------------------> t

Here is one with descriptions:

.. aafig::

                        SDA edge
         start                              stop
           |    |          |                 |
           v    v          v                 v
        ___      __________                   ___
    SDA    |    |          |                 |
           |____|          |_____..._________|
        ______      _____       _..._       _____
    SCL       |    |     |     |     |     |
              |____|     |_____|     |_____|

              ^    ^     ^     ^     ^     ^
              |    |     |     |     |     |
              | 'sh_in'  |  'sh_in'  |  'sh_in
           'sh_out'   'sh_out'    'sh_out'

                        SCL edge

Statistical diagrams
--------------------

Benfords_ distribution of the sizes of files on my hard drive:

.. _Benfords: http://en.wikipedia.org/wiki/Benfords_law

.. aafig::
    :foreground: #ff1050
    :aspect: 0.7

      |
    1 +------------------------------------------------------------> 31.59%
    2 +-------------------------------> 16.80%
    3 +-----------------------> 12.40%
    4 +-----------------> 9.31%
    5 +--------------> 7.89%
    6 +-----------> 6.10%
    7 +---------> 5.20%
    8 +---------> 4.90%
    9 +--------> 4.53%
      |         +         |         +         |         +         |
      +---------+---------+---------+---------+---------+---------+--->
      |         +         |         +         |         +         |
      0         5        10        15        20        25        30

Just some bars:

.. aafig::
    :fill: #00b

    ^     2
    |    EE
    | 1  EE       4
    |DD  EE   3  HH
    |DD  EE  GG  HH
    |DD  EE  GG  HH
    +------------------>


Schedules
---------

.. aafig::

    "Week"      |  1    |  2    |  3    |  4    |  5    |
    ------------+----------------------------------------
    "Task 1"    |HHHH
    "Task 2"    |    EEEEEEEEEEEE
    "Task 3"    |                GGGGGGGGZZZZZZZZZZ
    "Task 4"    |DD      DD          DD          DD
