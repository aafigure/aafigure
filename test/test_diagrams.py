#!/usr/bin/env python
#
# This file is part of aafigure. https://github.com/aafigure/aafigure
# (C) 2017 Chris Liechti <cliechti@gmx.net>
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


try:
    import PIL
except ImportError:
    pil_available = False
else:
    pil_available = True

try:
    import reportlab
except ImportError:
    reportlab_available = False
else:
    reportlab_available = True


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

    def test_render_api_svg(self):
        visitor, output = aafigure.render(ascii_art, options={'format': 'svg'})
        self.assertTrue(b'<svg' in output.getvalue())

    @unittest.skipUnless(pil_available, 'requires PIL or Pillow')
    def test_render_api_pil(self):
        visitor, output = aafigure.render(ascii_art, options={'format': 'png'})
        self.assertTrue(b'PNG' in output.getvalue())

    @unittest.skipUnless(reportlab_available, 'requires reportlab')
    def test_render_api_pdf(self):
        visitor, output = aafigure.render(ascii_art, options={'format': 'pdf'})
        self.assertTrue(b'%PDF' in output.getvalue())

    def test_process_api(self):
        output = BytesIO()
        visitor = aafigure.process(
            ascii_art,
            aafigure.svg.SVGOutputVisitor,
            options={'file_like': output})
        self.assertTrue(b'<svg' in output.getvalue())


if __name__ == '__main__':
    sys.stdout.write(__doc__)
    # When this module is executed from the command-line, it runs all its tests
    unittest.main()
