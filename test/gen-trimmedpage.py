#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
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
Generate a test PDF documents for pdfposter with more complex trimmed

This generates a PDF-file containing some DIN A4 pages with different
trim-boxes and content drawn outside the trim-box. The pages are
useful for checking if clipping works as expected.
"""

__author__ = "Hartmut Goebel <h.goebel@crazy-compilers.com>"
__copyright__ = "Copyright 2008-2013 by Hartmut Goebel <h.goebel@crazy-compilers.com>"
__licence__ = "GNU General Public License version 3 (GPL v3)"

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

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

def genTestFile(filename):
    stepSize = 2*cm
    bleed = 3*mm
    trimmargin = 2*cm
    cutmargin = trimmargin-bleed

    def genpage(canv, size,
                draw_trimbox, draw_bleedbox,
                set_trimbox, set_bleedbox, set_artbox,
                title):
        #--- draw the content
        # headline
        canv.setFillColor(lightblue)
        canv.rect(cutmargin, size[1]-cutmargin,
                  size[0]-2*cutmargin, -(4*cm+bleed),
                  fill=1, stroke=0)
        canv.setFillColor(black)
        canv.setFont("Helvetica", 12*mm)
        canv.drawCentredString(size[0]/2.0, size[1]-trimmargin-2.5*cm, title)
        canv.setFont("Helvetica", 5*mm)
        offset = 14*cm
        for v, n in (
            (set_trimbox, 'trim box'),
            (set_bleedbox, 'bleed box'),
            (set_artbox, 'art box'),
            ):
            if v:
                t = '%s: set' % n
            else:
                t = '%s: not set' % n
            canv.drawString(6*cm, offset, t)
            offset += 5*mm
            
        # main content
        canv.setFont("Helvetica", 7*mm)
        offset = 6*cm
        for x in range(3):
            for y in range(3):
                text = u"%x%x" % (x,y)
                if (x+y) % 2:
                    canv.setFillColor(pink)
                else:
                    canv.setFillColor(lightblue)
                canv.rect(offset+x*stepSize, offset+y*stepSize,
                          stepSize, stepSize, fill=True)
                canv.setFillColor(black)
                canv.drawCentredString(offset+(x+0.5)*stepSize,
                                       offset+(y+0.4)*stepSize, text)
        canv.drawCentredString(size[0]/2.0, offset-1.7*cm,
                               "His is a caption")

        # draw the artbox
        artRect = (offset-1*cm, offset-2.5*cm, 2*cm+3*stepSize, 3.5*cm+3*stepSize)
        draw_box(canv, (1,0,1), *artRect, text="art box")
        # draw trimbox
        if draw_trimbox:
            draw_box(canv, (0,1,0), 
                 trimmargin, trimmargin, size[0]-2*trimmargin, size[1]-2*trimmargin,
                 text="trim box")
        # draw bleedbox
        if draw_bleedbox:
            draw_box(canv, (0,0,1), 
                     cutmargin, cutmargin, size[0]-2*cutmargin, size[1]-2*cutmargin)

        # save the pdf file
        canv.showPage()
        return artRect

    def set_boxes(pageNum, size,
                draw_trimbox, draw_bleedbox,
                set_trimbox, set_bleedbox, set_artbox,
                title, artRect):
        page = reader.getPage(pageNum)
        print 'Page', i, size
        if set_bleedbox:
            page.bleedBox = RectangleObject(
                (cutmargin, cutmargin,
                 size[0]-cutmargin, size[1]-cutmargin))
            print ' bleed:', page.bleedBox
        if set_trimbox:
            page.trimBox = RectangleObject(
                (trimmargin, trimmargin,
                 size[0]-trimmargin, size[1]-trimmargin))
            print ' trim:', page.trimBox
        if set_artbox:
            page.artBox = RectangleObject(artRect)
            print ' art:', page.artBox
        writer.addPage(page)

    #----------- generate the first PDF w/o boxes defined -----------
    canv = Canvas(None, pagesize=A4)

    CASES = (
        # size, draw, set, title
        [A4, 1, 1, 1, 1,0, 'Full size'],
        [(A4[0]/2, A4[1]), 1, 1, 1,1,0, 'Half width'],
        [(A4[0]/2, A4[1]), 0, 0, 1,1,1, 'Half width'],
        [(A4[0]/2, A4[1]), 1, 1, 0,0,0, 'Half width'],
        [(A4[0]/2, A4[1]), 0, 0, 0,0,1, 'Half width'],
        )
    #--- draw the content
    for args in CASES:
        args.append(genpage(canv, *args))
    #canv.save() 
    pdfdata = canv.getpdfdata()
    
    #----------- generate the second PDF w/ trimbox, bleedbox, artbox set
    infile = StringIO.StringIO(pdfdata)
    reader = PdfFileReader(infile)
    writer = PdfFileWriter()
    for i, args in enumerate(CASES):
        set_boxes(i, *args)
    outputStream = open(filename, "wb")
    writer.write(outputStream)
    outputStream.close()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('filename',
                        help='Name of output file w/ box metrics')
    args = parser.parse_args()
    genTestFile(args.filename)
