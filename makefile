# This file is part of aafigure. https://github.com/aafigure/aafigure
# (C) 2006 Chris Liechti <cliechti@gmx.net>
#
# SPDX-License-Identifier:    BSD-3-Clause
#
# This makefile is for my convenience because my editor has a handy shortcut to
# run make.


# Clean up generated images, but only when the text file has been changed
# aafigure plugin for docutils must have been installed for this to work.
README.html: README.txt *.py aafigure/*.py
	rm -f aafigure-*.svg benford.svg
	rst2html.py --traceback README.txt README.html

# Create the manpage from the --help and --version outputs of the tool itself.
# Run the version in the working copy and not any installed version.
update-manpage:  aafigure.1
aafigure.1: FORCE
	PYTHONPATH=. help2man "python ./scripts/aafigure" --no-info \
		-i help2man.include >$@

# Get a preview of the man page.
show-manpage:
	groff -man -Tascii aafigure.1

# Sphinx docs
doc-html:
	cd documentation; $(MAKE) html

doc-pdf:
	cd documentation; $(MAKE) latex
	cd documentation/_build/latex; $(MAKE)

doc-clean:
	cd documentation; $(MAKE) clean

.PHONY: FORCE
