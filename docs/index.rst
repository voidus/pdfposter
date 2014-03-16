.. -*- mode: rst ; ispell-local-dictionary: "american" -*-

Welcome to pdftools.PDFposter's documentation!
==============================================

.. container:: admonition topic

  **Scale and tile PDF images/pages to print on multiple pages.**


`Pdfposter` can be used to create a large poster by building it from
multiple pages and/or printing it on large media. It expects as input a
PDF file, normally printing on a single page. The output is again a
PDF file, maybe containing multiple pages together building the
poster. The input page will be scaled to obtain the desired size.

This is much like the well-known tool `poster` does for Postscript
files, but working with PDF. Since sometimes poster does not like your
files converted from PDF. :-) Indeed `pdfposter` was inspired by `poster`.

Contents:

.. toctree::
   :maxdepth: 2

   Examples
   Frequently Asked Questions
   Development


Other tools for manipulating PDF
------------------------------------

* `pdfnup <http://pypi.python.org/pypi/pdfnup/>`_
* `pdfsplit <http://pypi.python.org/pypi/pdfsplit/>`_
* `pdfgrid <http://pypi.python.org/pypi/pdfgrid/>`_
