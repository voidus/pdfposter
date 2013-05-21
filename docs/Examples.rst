.. -*- mode: rst ; ispell-local-dictionary: "american" -*-

Examples
===============================

These are some examples showing how to get a poster as you want.

For these examples we use two input pages:

.. figure:: /images/testpage-tall.preview.png
  :align: center
  :alt: ..
  :scale: 33%
  :figwidth: 45%

  The *tall* example input page (5.0 cm x 27.9 cm)

.. figure:: /images/testpage-wide.preview.png
  :align: center
  :alt: ..
  :scale: 33%
  :figwidth: 45%

  The *wide* example input page (27.9 cm x 5.0 cm).


These are intentionally uncommon formats so the effects of running
`pdfposter` will be more demonstrative.

Working With Portrait Images
-------------------------------------

Portrait images are higher than wide.

Example 1::

    pdfposter -p 2x1a4 testpage-tall.pdf out.pdf

This are two a4 pages put together at the *long* side: Two portrait
pages wide and one portrait page high.

.. image:: /images/poster-tall-2x1a4.png
  :scale: 33%
  :alt: Tall test-page as poster: Two portrait pages wide and one portrait page high.

Example 2::

    pdfposter -p 1x2a4 testpage-tall.pdf out.pdf

This are two a4 pages put together at the *small* side: One portrait
page wide and two portrait pages high.

.. image:: /images/poster-tall-1x2a4.png
  :scale: 33%
  :alt: Tall test-page as poster: One portrait page wide and two portrait pages high.


Working With Landscape Images
------------------------------------

Landscape images are wider than hight.

Example 1::

    pdfposter -p 2x1a4 testpage-wide.pdf out.pdf

This are two a4 pages put together at the long side: Two portrait pages wide and one portrait page high.

.. image:: /images/poster-wide-2x1a4.png
  :scale: 33%
  :alt: Wide test-page as poster: Two portrait pages wide and one portrait page high.

Example 2::

    pdfposter -p 1x2a4 testpage-wide.pdf out.pdf

This are two a4 pages put together at the small side: One portrait page wide and two portrait pages high.


.. image:: /images/poster-wide-1x2a4.png
  :scale: 33%
  :alt: Wide test-page as poster: One portrait page wide and two portrait pages high.
