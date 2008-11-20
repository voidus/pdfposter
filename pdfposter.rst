.. -*- mode: rst -*-

==========================
pdfposter
==========================
-------------------------------------------------------------
Scale and tile PDF images/pages to print on multiple pages.
-------------------------------------------------------------
:Author:  Hartmut Goebel <h.goebel@goebel-consult.de>
:Version: Version 0.4.5
:Copyright: GNU Public Licence v3 (GPLv3)
:Manual section: 1

.. raw:: manpage

   .\" disable justification (adjust text to left margin only)
   .ad l


SYNOPSIS
==========

``pdfposter`` <options> infile outfile

DESCRIPTION
============

``Pdfposter`` can be used to create a large poster by building it from
multple pages and/or printing it on large media. It expects as input a
PDF file, normally printing on a single page. The output is again a
PDF file, maybe containing multiple pages together building the
poster.
The input page will be scaled to obtain the desired size.

.. comment
  The output pages bear cutmarks and have slightly overlapping
  images for easier assembling.

The program uses a simple but efficient method which is possible with
PDF: All new pages share the same data stream of the scaled page. Thus
resulting file grows moderatly.

To control its operation, you need to specify either the size of the
desired poster or a scale factor for the image:

- Given the poster size, it calculates the required number of sheets
  to print on, and from that a scale factor to fill these sheets
  optimally with the input image.

- Given a scale factor, it derives the required number of pages from
  the input image size, and positions the scaled image centered on
  this area.



OPTIONS
========

General Options
--------------------

--version             Show program's version number and exit
-h, --help            Show help message and exit
--help-media-names    List available media and disctance names and exit
-v, --verbose         Be verbose. Tell about scaling, rotation and number of
                      pages. Can be used more than once to increase the
                      verbosity.
-n, --dry-run     Show what would have been done, but do not generate files.

Defining Output
-----------------

-m BOX, --media-size=BOX  Specify the desired media size to print on.
          See below for *BOX*. The default is A4 in the standard
          package.

-p BOX, --poster-size=BOX    Specify the poster size. See below for *BOX*. 
         pdfposter will autonomously choose scaling and rotation to
         best fit the input onto the poster (see EXAMPLES below).

	 If you give neither the *-s* nor the *-p* option, the default
         poster size is identical to the media size.

-s NUMBER   Specify a linear scaling factor to produce the poster.
          Together with the input image size and optional margins,
          this induces an output poster size. So don't specify both *-s*
          and *-p*. 

	  Default is deriving the scale factor to fit a given poster
          size.

Box Definition
-----------------

The *BOX* mentioned above is a specification of horizontal and
vertical size. The syntax is as follows (with multipier being
specified optionally):

  *box* = [ *multiplier* ] *unit*

  *multiplier* = *number* "x" *number*

  *unit* = *medianame* or *distancename*

..
   Only in combination with the *-i* option, the program
   also understands the offset specification in the *BOX*.
    <offset> = +<number>,<number>
    [<offset>]
    and offset

Many international media names are recognised by the program, in upper
and lower case, and can be shortened to their first few characters, as
long as unique. For instance 'A0', 'Let'. Distance names are like
'cm', 'inch', 'ft'.

Medias are typically not quadratic but rectangular, which means width
and hight differ. Thus using medianames is a bit tricky:

:10x20cm: obviuos: 10 cm x 20 cm (portrait)
:20x10cm: same as 10x20cm, since all boxes are rotated to portrait
          format

Now when using medianames it gets tricky:

:1x1a4: same as approx. 21x29cm (21 cm x 29 cm, portrait)
:1x2a4: same as approx. 21x58cm (21 cm x 58 cm, portrait)

        This are two a4 pages put together at the *small* side: One
        portrait page wide and two portrait pages high.

:2x1a4: same as approx. 42x29cm, which is rotated to portrait and is
        the same a 29x42cm (29 cm x 42 cm)

        This are two a4 pages put together at the *long* side: Two
        portrait pages wide and one portrait page high.


EXAMPLES
============

:pdfposter -mA3 -pA0 a4.pdf out.pdf:
       Prints an A4 input file on 8 A3 pages, forming an A0 poster.

:pdfposter -p3x3Let a4.pdf out.pdf:
       Prints an inputfile on a poster of 3x3 Letter pages.

..
  not yet implemented: margins
  :pdfposter -mA0 -w2x2i input.pdf out.pdf:
       Enlarges an inputfile to print on a large-media A0 capable
       device, maintaining 2 inch margins:

:pdfposter -mA0 input.pdf out.pdf:
       Enlarges an inputfile to print on a large-media A0 capable
       device.

:pdfposter -s4 input.pdf out.pdf:
       Enlarge an inputfile exactly 4 times, print on the default A4
       media, and let ``pdfposter`` determine the number of pages
       required.

..
   not yet implemented
   :pdfposter -mLegal -p1x1m -w10% -C5 input.pdf out.pdf:
       Scale a postscript image to a poster of about 1 square meter,
       printing on 'Legal' media, maintaining a 10% of 'Legal' size
       as white margin around the poster. Print cutmark lines and grid
       labels, but don't print cut mark arrow heads.


:pdfposter -m10x10cm -pa0 a4.pdf out.pdf:
  Just to show how efficient ``pdfposter`` is: This will create a file
  containing 192 pages, but only 15 times as big as the single page.
  With a4.pdf being a quite empty page, this ratio should be even
  better for filled pages.

More examples including sample pictures can be found at
http://pdfposter.origo.ethz.ch/wiki/examples

Examples for automatic scaling
------------------------------------

* For printing 2 *portrait* A4 pages high (approx. 58cm) and let
  pdfposter determine how many portrait pages wide, specify a lage
  number of *vertical* pages. eg:

     :pdfposter -p999x2a4 testpage-wide.pdf out.pdf:

* For printing 2 *landscape* A4 pages high (approx. 20cm) and let
  pdfposter determine how many landscape pages wide, specify a lage
  number of *horizontal* pages. eg:

     :pdfposter -p2x999a4 testpage-wide.pdf out.pdf:


SEE ALSO
=============

``poster``\(1)

Project Homepage http://pdfposter.origo.ethz.ch/
