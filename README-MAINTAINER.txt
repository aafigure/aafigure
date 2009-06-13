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
1. Make sure the branch is up-to date and all changes are committed.
2. Ensure the version is incremented:
   - setup.py  must be updated
   - CHANGES.txt must contain a summary of the changes
   - debian/changes must be updated with (may use ``dch``)
3. Tag the sources.
4. Build a source package: ``bzr builddeb -S``
3. Upload to PPA: ``dput aafigure-ppa ./aafigure_0.2_source.changes``
4. Wait... Then check https://launchpad.net/~aafigure-team/+archive/ppa
4. Don't forget to bzr push

For a local test, ``debuild`` respectively ``debuild -S`` can be run in the
``aafigure`` directory. The resulting debian package is placed in the parent
directory.


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

