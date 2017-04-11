#!/usr/bin/env python
#
# This file is part of aafigure
#
# SPDX-License-Identifier:    BSD-3-Clause
"""
Test a few basic diagrams.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import unittest
import aafigure
import aafigure.aa
import aafigure.svg
from io import BytesIO, StringIO

ascii_art = u"""\
    ---> | ^|   |
    <--- | || --+--
    <--> | |V   |
 __             __
|  |__  +---+  |__|
        |box|   ..
        +---+  Xenophon
"""


class TestDiagrams(unittest.TestCase):

    def test_ascii_steps(self):
        aaimg = aafigure.AsciiArtImage(ascii_art)
        aaimg.recognize()

        output = StringIO()
        aav = aafigure.aa.AsciiOutputVisitor({'file_like': output, 'scale': 2})
        aav.visit_image(aaimg)

    def test_render_api(self):
        visitor, output = aafigure.render(ascii_art, options={'format': 'svg'})


if __name__ == '__main__':
    sys.stdout.write(__doc__)
    # When this module is executed from the command-line, it runs all its tests
    unittest.main()
