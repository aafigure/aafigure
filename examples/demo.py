#!/usr/bin/env python

"""\
Demonstration code for aafigure use as python module.
"""

import sys
import aafigure
import aafigure.aa

ascii_art = """\
    ---> | ^|   |
    <--- | || --+--
    <--> | |V   |
 __             __
|  |__  +---+  |__|
        |box|   ..
        +---+  Xenophon
"""

# Show what we're parsing.
print " input ".center(78, '=')
print ascii_art
# Parse the image.
aaimg = aafigure.AsciiArtImage(ascii_art)
aaimg.recognize()

# For fun, output the ASCII version in the console.
print " output ".center(78, '=')
aav = aafigure.aa.AsciiOutputVisitor({'file_like':sys.stdout, 'scale':2})
aav.visit_image(aaimg)
print "="*78

# Writing an SVG file would be possible in a similar way, but there is the much
# easier render function for that.

# A stringIO object is returned for the output when the output parameter is not
# given. If it were, the output would be directly written to that object.
visitor, output = aafigure.render(ascii_art, options={'format':'svg'})

# The process method can be used for a lower level access. The visitor class
# has to be specified by the user in this case.  To get output, a file like
# object has to be passed in the options:
# {'file_like' = open("somefile.svg", "wb")}
import aafigure.svg
import StringIO
fl = StringIO.StringIO()
visitor = aafigure.process(
    ascii_art,
    aafigure.svg.SVGOutputVisitor,
    options={'file_like': fl}
)
