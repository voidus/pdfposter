#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2013 by Elena Grandi <elena.valhalla@gmail.com>
# Copyright 2008-2012 by Hartmut Goebel <h.goebel@crazy-compilers.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
"""
Generate example PDF documents for pdfposter.

This generates two PDF-files:
- a tall one (5.0 cm x 29,7 cm)
- a wide one (29.7 cm x 5.0 cm)

These pages are later used creating images for examples.
"""

__author__ = "Hartmut Goebel <h.goebel@crazy-compilers.com>"
__copyright__ = "Copyright 2008-2012 by Hartmut Goebel <h.goebel@crazy-compilers.com>"
__licence__ = "GNU General Public License version 3 (GPL v3)"

from reportlab.lib.units import mm
from reportlab.lib.colors import black
from reportlab.pdfgen.canvas import Canvas

def genTestFile(filename_tall, filename_wide):
    short_size = 50*mm
    long_size = 297*mm
    numbers = ['B', 'A', '9', '8', '7', '6', '5', '4', '3', '2', '1']
    margin = 10*mm

    #----------- generate the tall PDF -----------
    size = (short_size, long_size)
    step = (long_size - margin*2)/len(numbers)
    canv = Canvas(filename_tall, pagesize=size)
    canv.setFont("Helvetica", 72)
    canv.setStrokeColor(black)

    # draw the content
    for i, n in enumerate(numbers):
        canv.drawCentredString(short_size/2, step*i + margin + 4*mm, n)
    canv.rect(margin, margin, short_size - margin * 2,
            long_size - margin * 2, fill=0, stroke=1)

    # save the pdf file
    canv.showPage()
    canv.save()

    #----------- generate the wide PDF -----------
    size = (long_size, short_size)
    step = (long_size - margin*2)/len(numbers)
    numbers.reverse()
    canv = Canvas(filename_wide, pagesize=size)
    canv.setFont("Helvetica", 72)
    canv.setStrokeColor(black)

    # draw the contents
    for i, n in enumerate(numbers):
        canv.drawCentredString(step*i + margin + step/2, margin + 6*mm, n)
    canv.rect(margin, margin, long_size - margin * 2,
            short_size - margin * 2, fill=0, stroke=1)

    # save the pdf file
    canv.showPage()
    canv.save()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('filename_tall',
                        help='Name of tall output file')
    parser.add_argument('filename_wide',
                        help='Name of wide output file')
    args = parser.parse_args()
    genTestFile(args.filename_tall, args.filename_wide)
