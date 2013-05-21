.. -*- mode: rst ; ispell-local-dictionary: "american" -*-

Frequently Asked Questions
===============================

* *How can I suppress these superfluous empty pages?*

  *Short Answer:* Specify the desired output size using the same
  page-name as the medium-size::

     pdfposter -mA5 -p2xA5 in.pdf out.pdf

  *Long Answer*: If you are running::

     pdfposter -mA5 -pA4 in.pdf out.pdf

  you most probably expect the result to be 2 A5-pages large, but you
  will get *three* pages, where the third seams to be empty. (If you
  have a full-colored background, you will find a small line on the
  third page.)

  And this is what went wrong:

  In the command above, you *say*: "The output should be A4 sized",
  while you *mean*: "The output should fit on two A5 pages".

  Basically you are right, if you say "hey, this ought to be the
  same!". It is a scaling or rounding issue caused by ISO page sizes
  not scaling exactly (even as they should, see `ISO_216
  http://en.wikipedia.org/wiki/ISO_216>`_). For example since A4 is
  297 mm high, A5 should be 148.5 mm wide, but is only 148 mm wide.

  So the solution is to specify on the command-line what you want:
  "should fit on two A5 pages"::

         pdfposter -mA5 -p2xA5 in.pdf out.pdf


* Are there other Python tools for manipulating PDF?

  Yes, there are: These tools even use the `pyPDF package
  <http://pybrary.net/pyPdf/>`_ as pdfposter does. Thus installing
  them will only require a small amount of disk space.

  * `pdfnup <http://pypi.python.org/pypi/pdfnup/`_
  * `pdfsplit <http://pypi.python.org/pypi/pdfsplit/`_
  * `pdfgrid <http://pypi.python.org/pypi/pdfgrid/>`_
