.. -*- mode: rst -*-

==========================
pdfposter
==========================

-------------------------------------------------------------
Scale and tile PDF images/pages to print on multiple pages.
-------------------------------------------------------------

:Author:  Hartmut Goebel <h.goebel@goebel-consult.de>
:Version: Version 0.4
:Copyright: GNU Public Licence v3 (GPLv3)
:Homepage: http://pdfposter.origo.ethz.ch/

``Pdfposter`` can be used to create a large poster by building it from
multple pages and/or printing it on large media. It expects as input a
PDF file, normally printing on a single page. The output is again a
PDF file, maybe containing multiple pages together building the
poster.
The input page will be scaled to obtain the desired size.

This is much like ``poster`` does for Postscript files, but working
with PDF. Since sometimes poster does not like your files converted
from PDF. :-) Indeed ``pdfposter`` was inspired by ``poster``.

For more information please refere to the manpage or visit
the `project homepage <http://pdfposter.origo.ethz.ch/>`_.


Requirements
~~~~~~~~~~~~~~~~~~~~

``Pdfposter`` requires

* Python 2.x (tested with 2.5, but other versions should work, too),
* `pyPdf <http://pybrary.net/pyPdf/>`_ > 1.10,
* setuptools for installation (see below).


Installation
~~~~~~~~~~~~~~~~~~~

Installation Requirements
----------------------------

``Pdfposter`` uses setuptools for installation. Thus you need
either

  * network access, so the install script will automatically download
    and install setuptools if they are not already installed

or

  * the correct version of setuptools preinstalled using the `EasyInstall
    installation instructions  <http://peak.telecommunity.com/DevCenter/EasyInstall#installation-instructions>`_. 
    Those instructions also have tips for
    dealing with firewalls as well as how to manually download and
    install setuptools.


Installation 
-------------------------

Install ``pdfposter`` by just running::

   python ./setup.py install



Custom Installation Locations
------------------------------

``pdfposter`` is just a single script (aka Python program). So you can
copy it where ever you want (maybe fixing the first line). But it's
easier to just use::

   # install to /usr/local/bin
   python ./setup.py install --prefix /usr/local

   # install to your Home directory (~/bin)
   python ./setup.py install --home ~


Please mind: This effects also the installation of pfPDf (and
setuptools) if they are not already installed.

For more information about Custom Installation Locations please
refere to the `Custom Installation Locations Instructions
<http://peak.telecommunity.com/DevCenter/EasyInstall#custom-installation-locations>`_.
before installing ``pdfposter``.
