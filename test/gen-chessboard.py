#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
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
Generate test PDF documents for pdfcrop.
"""

__author__ = "Hartmut Goebel <h.goebel@crazy-compilers.com>"
__copyright__ = "Copyright 2008-2012 by Hartmut Goebel <h.goebel@crazy-compilers.com>"
__licence__ = "GNU General Public License version 3 (GPL v3)"

from reportlab.lib.units import mm, cm
from reportlab.lib.colors import black, white, pink, lightblue, blue
from reportlab.lib.pagesizes import A4, legal, landscape
from reportlab.pdfgen.canvas import Canvas


def genTestFile(path, numPages):
    """Generate a PDF doc with a chess-board laout numbers on each page.
    Usefull for debugging cropped pages."""
    
    stepSize = 2*cm
    size = A4
    #size = (size[0] + lm + rm, size[1] + tm +bm)
    canv = Canvas(path, pagesize=size)
    for i in range(numPages):
        canv.setFont("Helvetica", 7*mm)
        canv.setStrokeColor(black)
        for x in range(int(size[0] / stepSize)):
            for y in range(int(size[1] / stepSize)):
                text = u"%x%x" % (x,y)
                if (x+y) % 2 == 1:
                    canv.setFillColor(pink)
                else:
                    canv.setFillColor(lightblue)
                canv.rect(x*stepSize, y*stepSize, stepSize, stepSize, fill=True)
                if i % 2 == 1:
                    canv.setFillColor(black)
                else:
                    canv.setFillColor(blue)
                canv.drawCentredString((x+0.5)*stepSize, (y+0.4)*stepSize, text)
        canv.showPage()
    canv.save() 


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-n','--num-pages',
                        default=1, type=int,
                        help='number of pages to generate (default: %(default)s)')
    parser.add_argument('filename',
                        default="chessboard.pdf",
                        help='Name of output file (default: %(default)s')
    args = parser.parse_args()
    genTestFile(args.filename, args.num_pages)
