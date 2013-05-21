#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2013 by Elena Grandi <elena.valhalla@gmail.com>
# Copyright 2008-2013 by Hartmut Goebel <h.goebel@crazy-compilers.com>
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
Generate test PDF documents for pdfposter.

This generates a PDF-file containing a portrait and a landscape page,
DIN A4.
"""

__author__ = "Hartmut Goebel <h.goebel@crazy-compilers.com>"
__copyright__ = "Copyright 2008-2013 by Hartmut Goebel <h.goebel@crazy-compilers.com>"
__licence__ = "GNU General Public License version 3 (GPL v3)"

from reportlab.lib.units import mm
from reportlab.lib.colors import black
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas

def draw_numbers(canvas, numbers, size, margin, rows, cols):
    step_x = (size[0] - margin*2)/cols
    step_y = (size[1] - margin*2)/rows
    for i, n in enumerate(numbers):
        canvas.drawCentredString(margin + step_x / 2 + step_x * (i%cols),
                margin + step_y / 2 + ( rows - 1 - i / cols) * step_y, n)

def genTestFile(filename):
    size = A4
    numbers = ['1', '2', '3', '4', '5', '6']
    margin = 20*mm

    #----------- generate the PDF -----------
    # 1st page (portrait)
    canv = Canvas(filename, pagesize=size)
    canv.setFont("Helvetica", 72)
    canv.setStrokeColor(black)

    # draw the content
    draw_numbers(canv,numbers,size,margin,3,2)
    canv.rect(margin, margin, size[0] - margin * 2,
            size[1] - margin * 2, fill=0, stroke=1)

    # close page
    canv.showPage()

    # second page (landscape)
    size = (size[1],size[0])
    canv.setPageSize(size)
    canv.setFont("Helvetica", 72)
    canv.setStrokeColor(black)

    # draw the content
    draw_numbers(canv,numbers,size,margin,2,3)
    canv.rect(margin, margin, size[0] - margin * 2,
            size[1] - margin * 2, fill=0, stroke=1)

    # close page, save PDF
    canv.showPage()
    canv.save()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('filename',
                        help='Name of output file')
    args = parser.parse_args()
    genTestFile(args.filename)
