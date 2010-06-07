.. -*- mode: rst -*-

==========================
pdfposter
==========================

-------------------------------------------------------------
Scale and tile PDF images/pages to print on multiple pages.
-------------------------------------------------------------

:Author:  Hartmut Goebel <h.goebel@goebel-consult.de>
:Version: Version 0.5.0
:Copyright: GNU Public Licence v3 (GPLv3)
:Homepage: http://pdfposter.origo.ethz.ch/

``Pdfposter`` can be used to create a large poster by building it from
multiple pages and/or printing it on large media. It expects as input a
PDF file, normally printing on a single page. The output is again a
PDF file, maybe containing multiple pages together building the
poster.
The input page will be scaled to obtain the desired size.

This is much like ``poster`` does for Postscript files, but working
with PDF. Since sometimes poster does not like your files converted
from PDF. :-) Indeed ``pdfposter`` was inspired by ``poster``.

For more information please refer to the manpage or visit
the `project homepage <http://pdfposter.origo.ethz.ch/>`_.


Requirements and Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``Pdfposter`` requires

* `Python 2.x`__ or higher (tested with 2.5 and 2.6, but other
   versions should work, too, Python 3.x is *not* supported),
* `setuptools`__ for installation (see below), and
* `pyPdf`__ >= 1.11.

__ http://www.python.org/download/
__ http://pybrary.net/pyPdf/
__ http://pypi.python.org/pypi/setuptools


:Hints for installing on Windows: Following the links above you will
   find .msi and .exe-installers. Simply install them and continue
   with `installing pdfposter`_.

:Hints for installing on GNU/Linux: Most current GNU/Linux distributions
   provide packages for the requirements. Look for packages names like
   `python-setuptools` and `python-pypdf`. Simply install them and
   continue with `installing pdfposter`_.

:Hint for installing on other platforms: Many vendors provide Python.
   Please check your vendors software repository. Otherwise please
   download Python 2.6 (or any higer version from the 2.x series) from
   http://www.python.org/download/ and follow the installation
   instructions there.

   After installing Python, install `setuptools`__. You may want to
   read `More Hints on Installing setuptools`_ first.

__ http://pypi.python.org/pypi/setuptools

   Using setuptools, compiling and installing the remaining
   requirements is a piece of cake::

     # if the system has network access
     easy_install pyPdf

     # without network access download pyPdf
     # from http://pybrary.net/pyPdf/ and run
     easy_install pyPdf-*.zip


Installing pdfposter
---------------------------------

When you are reading this you most probably already downloaded and
unpacked `pdfposter`. Thus installing is as easy as running::

   python ./setup.py install

Otherwise you may install directly using setuptools/easy_install. If
your system has network access installing `pdfposter` is a
breeze::

     easy_install pdfposter

Without network access download `pdfposter` from
http://pypi.python.org/pypi/pdfposter and run::

     easy_install pdfposter-*.tar.gz


More Hints on Installing setuptools
------------------------------------

`pdfposter` uses setuptools for installation. Thus you need
either

  * network access, so the install script will automatically download
    and install setuptools if they are not already installed

or

  * the correct version of setuptools preinstalled using the
    `EasyInstall installation instructions`__. Those instructions also
    have tips for dealing with firewalls as well as how to manually
    download and install setuptools.

__ http://peak.telecommunity.com/DevCenter/EasyInstall#installation-instructions


Custom Installation Locations
------------------------------

``pdfposter`` is just a single script (aka Python program). So you can
copy it where ever you want (maybe fixing the first line). But it's
easier to just use::

   # install to /usr/local/bin
   python ./setup.py install --prefix /usr/local

   # install to your Home directory (~/bin)
   python ./setup.py install --home ~


Please mind: This effects also the installation of pyPdf (and
setuptools) if they are not already installed.

For more information about Custom Installation Locations please refer
to the `Custom Installation Locations Instructions`__ before
installing ``pdfposter``.

__ http://peak.telecommunity.com/DevCenter/EasyInstall#custom-installation-locations>
