#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2008-2012 by Hartmut Goebel <h.goebel@goebel-consult.de>
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
Generate test PDF documents for pdfposter
"""

__author__ = "Hartmut Goebel <h.goebel@goebel-consult.de>"
__copyright__ = "Copyright 2008-2012 by Hartmut Goebel <h.goebel@goebel-consult.de>"
__licence__ = "GNU General Public License version 3 (GPL v3)"

from reportlab.lib.units import mm, cm
from reportlab.lib.colors import black, white, pink, lightblue, blue
from reportlab.lib.pagesizes import A4, legal, landscape
from reportlab.pdfgen.canvas import Canvas

from pyPdf import PdfFileWriter, PdfFileReader
from pyPdf.generic import RectangleObject

def draw_box(canvas, color, x,y, width,height, text=None):
    canvas.setStrokeColorRGB(*color)
    canvas.rect(x,y, width,height)
    if text:
        canvas.setFillColorRGB(*color)
        canvas.setFont("Helvetica", 3*mm)
        canvas.drawString(x+1*mm, y+1*mm, text)

def genTestFile(filename1, filename2):
    stepSize = 2*cm
    size = A4
    bleed = 3*mm
    trimmargin = 2*cm
    cutmargin = trimmargin-bleed

    #----------- generate the first PDF w/o boxes defined -----------
    canv = Canvas(filename1, pagesize=size)
    canv.setFont("Helvetica", 7*mm)
    canv.setStrokeColor(black)

    #--- draw the content
    # headline
    canv.setFillColor(lightblue)
    canv.rect(cutmargin, size[1]-cutmargin, size[0]-2*cutmargin, -(4*cm+bleed),
              fill=1, stroke=0)
    canv.setFillColor(black)
    canv.setFont("Helvetica", 12*mm)
    canv.drawCentredString(size[0]/2.0, size[1]-trimmargin-2.5*cm,
                           "This is a headline")
    # main content
    canv.setFont("Helvetica", 7*mm)
    offset = 6*cm
    for x in range(5):
        for y in range(6):
            text = u"%x%x" % (x,y)
            if (x+y) % 2:
                canv.setFillColor(pink)
            else:
                canv.setFillColor(lightblue)
            canv.rect(offset+x*stepSize, offset+y*stepSize, stepSize, stepSize, fill=True)
            canv.setFillColor(black)
            canv.drawCentredString(offset+(x+0.5)*stepSize, offset+(y+0.4)*stepSize, text)
    canv.drawCentredString(size[0]/2.0, offset-1.7*cm,
                           "His is a caption")

    # draw the artbox
    artRect = (offset-1*cm, offset-2.5*cm, 2*cm+5*stepSize, 3.5*cm+6*stepSize)
    draw_box(canv, (1,0,1), *artRect, text="art box")
    # draw trimbox
    draw_box(canv, (0,1,0), 
             trimmargin, trimmargin, size[0]-2*trimmargin, size[1]-2*trimmargin,
             text="trim box")
    # draw bleedbox
    draw_box(canv, (0,0,1), 
             cutmargin, cutmargin, size[0]-2*cutmargin, size[1]-2*cutmargin)

    # draw horizonal cut marks
    canv.line(0,      trimmargin,         cutmargin,        trimmargin)
    canv.line(size[0],trimmargin,         size[0]-cutmargin,trimmargin)
    canv.line(0,      size[1]-trimmargin, cutmargin,        size[1]-trimmargin)
    canv.line(size[0],size[1]-trimmargin, size[0]-cutmargin,size[1]-trimmargin)
    # draw vertical cut marks
    canv.line(trimmargin,        0,       trimmargin,        cutmargin)
    canv.line(size[0]-trimmargin,0,       size[0]-trimmargin,cutmargin)
    canv.line(trimmargin,        size[1], trimmargin,        size[1]-cutmargin)
    canv.line(size[0]-trimmargin,size[1], size[0]-trimmargin,size[1]-cutmargin)

    # save the pdf file
    canv.showPage()
    canv.save() 

    #----------- generate the second PDF w/ trimbox, bleedbox, artbox set
    reader = PdfFileReader(open(filename1, "rb"))
    writer = PdfFileWriter()
    page = reader.getPage(0)

    x0, y0, x1, y1 = map(float, page.mediaBox)
    assert x0 == 0
    assert y0 == 0
    assert round(x1, 2) == round(size[0], 2)
    assert round(y1, 2) == round(size[1], 2)
    page.bleedBox = RectangleObject((x0+cutmargin, y0+cutmargin,
                                     x1-cutmargin, y1-cutmargin))
    page.trimBox = RectangleObject((x0+trimmargin, y0+trimmargin,
                                    x1-trimmargin, y1-trimmargin))
    page.artBox = RectangleObject(artRect)
    writer.addPage(page)

    outputStream = open(filename2, "wb")
    writer.write(outputStream)
    outputStream.close()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('filename1',
                        help='Name of output file w/o box metrics within')
    parser.add_argument('filename2',
                        help='Name of output file w/ box metrics')
    args = parser.parse_args()
    genTestFile(args.filename1, args.filename2)
