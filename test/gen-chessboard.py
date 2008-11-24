#!/usr/bin/env python
# _*_ coding: UTF-8 _*_

"Generate test PDF documents for pdfcrop."

from reportlab.lib.units import mm, cm
from reportlab.lib.colors import black, white, pink, lightblue, blue
from reportlab.lib.pagesizes import A4, legal, landscape
from reportlab.pdfgen.canvas import Canvas


# not used anymore
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
        for x in range(size[0] / stepSize):
            for y in range(size[1] / stepSize):
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
    genTestFile("chessboard.pdf", 4)
