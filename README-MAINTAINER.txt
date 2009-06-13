==========================
 aafigure maintainer docs
==========================

This document contains notes for developers and packagers. End users probably
want to read README.txt instead.


What's in the branch
====================
aafigure
    This is the main part. The ``aafigure`` directory contains the python
    package. The setup.py and other files in the root directory belong to it.

docutils-aafigure
    This is a plugin for docutils, that provides a ``aafigure`` directive.
    It is maintained in the ``docutils`` directory.


Debian Package
==============
The Debian package currently covers the aafigure package only. It is built
using bzr-builddeb (this ensures that only files under version control get
included in the source.tar.gz and no other files possibly present in the
working copy).

For a release:
1. Make sure the branch is up-to date.
2. Ensure the version is incremented:
   - setup.py  must be updated
   - aafigure/aafigure.py  must be updated, see version at end of file
   - CHANGES.txt  must contain a summary of the changes
   - debian/changes  must be updated (may use ``dch -v 0.3``)
3. Make sure all changes are committed, including the verison number changes.
4. Tag the sources.
5. Build a source package: ``bzr builddeb -S``.
6. Upload to PPA: ``dput aafigure-ppa ./aafigure_0.2_source.changes``.
7. Wait... Then check https://launchpad.net/~aafigure-team/+archive/ppa
8. Don't forget to ``bzr push``.
9. PyPi rellease done?

For a local test, ``debuild`` respectively ``debuild -S`` can be run in the
``aafigure`` directory. The resulting debian package is placed in the parent
directory.


PyPi Release
============
See debian package release and ensure that version numbers are correct.

1. ``python setup.py register``
2. ``python setup.py sdist upload``


dput settings
=============
The ``dput`` tool needs a configuration file: ``~/.dput.cf``::

    [DEFAULT]
    default_host_main = notspecified

    [notspecified]
    fqdn = SPECIFY.A.PPA.NAME
    incoming = .

    [aafigure-ppa]
    fqdn = ppa.launchpad.net
    method = ftp
    incoming = ~aafigure-team/ppa/ubuntu/
    login = anonymous
    allow_unsigned_uploads = 0


References
==========
- bzr-builddeb Homepage: https://launchpad.net/bzr-builddeb
- bzr-builddeb Documentation: http://jameswestby.net/bzr/builddeb


