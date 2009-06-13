"""\
Demonstarion code for aafigure use as python module.
"""

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
aav = aafigure.aa.AsciiOutputVisitor(scale=2)
aav.visit_image(aaimg)
print aav
print "="*78

# Writing an SVG file would be possible in a similar way, but there is the much
# easier render function for that.

# A stringIO object is returned for the output when the output parameter is not
# given. If it were, the output would be directly written to that object.
visitor, output = aafigure.render(ascii_art, options={'format':'svg'})
