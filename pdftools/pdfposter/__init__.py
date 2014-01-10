#!/usr/bin/env python
"""
pdftools.pdfposter - scale and tile PDF images/pages to print on multiple pages.
"""
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

__author__ = "Hartmut Goebel <h.goebel@crazy-compilers.com>"
__copyright__ = "Copyright 2008-2013 by Hartmut Goebel <h.goebel@crazy-compilers.com>"
__licence__ = "GNU General Public License version 3 (GPL v3)"
__version__ = "0.6.1dev"

# ignore some warnings for pyPDF < 1.13
import warnings
warnings.filterwarnings('ignore', "the sets module is deprecated")
warnings.filterwarnings('ignore', "the md5 module is deprecated")

from pyPdf.pdf import PdfFileWriter, PdfFileReader, PageObject, getRectangle, \
     ArrayObject, ContentStream, NameObject, FloatObject, RectangleObject

import logging
from logging import log
import math

DEFAULT_MEDIASIZE = 'a4'

mm = 72 / 25.4

# Taken from poster.c
papersizes = {
    'pt'  : (1, 1),
    'inch': (72, 72),
    'ft'  : (864, 864), # 12 inch
    'mm'  : (mm, mm),
    'cm'  : (10 *mm, 10 *mm),
    'meter':(1000* mm, 1000* mm),

    # American page sizes (taken from psposter.c)
    "monarch"  : (279, 540),
    "statement": (396, 612),
    "executive": (540, 720),
    "quarto"   : (610, 780),
    "letter"   : (612, 792),
    "folio"    : (612, 936),
    "legal"    : (612, 1008),
    "tabloid"  : (792, 1224),
    "ledger"   : (792, 1224),

    # ISO page sizes (taken from psposter.c)
    "a0" : (2384, 3370),
    "a1" : (1684, 2384),
    "a2" : (1191, 1684),
    "a3" : (842, 1191),
    "a4" : (595, 842),
    "a5" : (420, 595),
    "a6" : (298, 420),
    "a7" : (210, 298),
    "a8" : (147, 210),
    "a9" : (105, 147),
    "a10": (74, 105),

    "dinlang"   : (281, 595), # 1/3 a4
    "envdinlang": (312, 624), # envelobe for din-lang

    "b0" : (2835, 4008),
    "b1" : (2004, 2835),
    "b2" : (1417, 2004),
    "b3" : (1001, 1417),
    "b4" : (709, 1001),
    "b5" : (499, 709),
    "b6" : (354, 499),
    "b7" : (249, 354),
    "b8" : (176, 249),
    "b9" : (125, 176),
    "b10": (88, 125),

    "c4" : (649, 918),
    "c5" : (459, 649),
    "c6" : (323, 459),

    # Japanese page sizes (taken from psposter.c)
    "jb0" : (2920, 4127),
    "jb1" : (2064, 2920),
    "jb2" : (1460, 2064),
    "jb3" : (1032, 1460),
    "jb4" : (729, 1032),
    "jb5" : (516, 729),
    "jb6" : (363, 516),
    "jb7" : (258, 363),
    "jb8" : (181, 258),
    "jb9" : (128, 181),
    "jb10": (91, 128),

    "comm10": (298, 684),
    "com10" : (298, 684),
    "env10" : (298, 684),
    }

class DecryptionError(ValueError): pass
    

PAGE_BOXES = ("/MediaBox", "/CropBox", "/BleedBox", "/TrimBox", "/ArtBox")

def rectangle2box(pdfbox):
    return {
        'width'   : pdfbox.getUpperRight_x()-pdfbox.getLowerLeft_x(),
        'height'  : pdfbox.getUpperRight_y()-pdfbox.getLowerLeft_y(),
        'offset_x': pdfbox.getLowerLeft_x(),
        'offset_y': pdfbox.getLowerLeft_y(),
        # the following are unused, but need to be set to make
        # `rotate_box()` work
        'units_x' : None,
        'units_y' : None,
        }

def rotate_box(box):
    for a,b in (
        ('width', 'height'),
        ('offset_x', 'offset_y'),
        ('units_x', 'units_y')):
        box[a], box[b] = box[b], box[a]

def rotate2portrait(box, which):
    'if box is landscape spec, rotate to portrait'
    if (  box['width' ]-box['offset_x'] 
        > box['height']-box['offset_y']):
        rotate_box(box)
        log(18, 'Rotating %s specs to portrait format', which)
        return True

def decide_num_pages(inbox, mediabox, posterbox, scale=None):
    """decide on number of pages"""
    # avoid changing original posterbox when handling multiple pages
    # (if --scale, posterbox is None)
    posterbox = posterbox and posterbox.copy()
    cutmargin   = {'x': 0, 'y': 0} # todo
    whitemargin = {'x': 0, 'y': 0} # todo
    # media and image sizes (inbox) are fixed already
    # available drawing area per sheet
    drawable_x = mediabox['width' ] - 2*cutmargin['x']
    drawable_y = mediabox['height'] - 2*cutmargin['y']

    rotate = False

    inbox_x = float(inbox['width' ])
    inbox_y = float(inbox['height'])
    log(17, 'input  dimensions: %.2f %.2f (trimbox of input page)',
            inbox_x, inbox_y)

    if not scale:
        # user did not specify scale factor, calculate from output size
        # todo: fix assuming posterbox offset = 0,0
        log(17, 'output dimensions: %.2f %.2f (poster size)',
            posterbox['width'], posterbox['height'])

        # ensure poster spec are portrait
        if rotate2portrait(posterbox, 'poster'):
            rotate = rotate != True # xor

        # if the input page has landscape format rotate the
        # poster spec to landscape, too
        if inbox_x > inbox_y:
            log(18, 'Rotating poster specs since input page is landscape')
            rotate = rotate != True # xor
            rotate_box(posterbox)
            log(18, 'rotated output dimensions: %.2f %.2f (poster size)',
                posterbox['width'], posterbox['height'])

        scale = min(posterbox['width' ] / inbox_x,
                    posterbox['height'] / inbox_y)
        log(18, 'Calculated page scaling factor: %f', scale)

    # use round() to avoid floating point roundup errors
    size_x = round(inbox_x*scale - whitemargin['x'], 4)
    size_y = round(inbox_y*scale - whitemargin['y'], 4)
    log(17, 'output dimensions: %.2f %.2f (calculated)', size_x, size_y)

    # num pages without rotation
    nx0 = int(math.ceil( size_x / drawable_x))
    ny0 = int(math.ceil( size_y / drawable_y))
    # num pages with rotation
    nx1 = int(math.ceil( size_x / drawable_y))
    ny1 = int(math.ceil( size_y / drawable_x))

    log(17, 'Pages w/o rotation %s x %s' , nx0, ny0)
    log(17, 'Pages w/  rotation %s x %s' , nx1, ny1)

    # Decide for rotation to get the minimum page count.
    # (Rotation is considered as media versus input page, which is
    # totally independent of the portrait or landscape style of the
    # final poster.)
    rotate = (rotate and (nx0*ny0) == (nx1*ny1)) or (nx0*ny0) > (nx1*ny1)
    log(17, 'Decided for rotation: %s', rotate and 'yes' or 'no')

    if rotate:
        ncols = nx1
        nrows = ny1
    else:
        ncols = nx0
        nrows = ny0

    log(19, "Deciding for %d column%s and %d row%s of %s pages.",
            ncols, (ncols==1) and "s" or "",
            nrows, (nrows==1) and "s" or "",
            rotate and "landscape" or "portrait")
    return ncols, nrows, scale, rotate


def copyPage(page):
    from pyPdf.pdf import RectangleObject, NameObject
    newpage = PageObject(page.pdf)
    newpage.update(page)
    # Copy Rectangles to be manipulatable
    for attr in PAGE_BOXES:
        if page.has_key(attr):
            newpage[NameObject(attr)] = RectangleObject(list(page[attr]))
    return newpage

def _clip_pdf_page(page, x, y, width, height):
    content = ContentStream(page["/Contents"].getObject(), page.pdf)
    content.operations[:0] = [
        ([], 'q'), # save graphic state
        ([], 'n'), # cancel path w/ filling or stroking
        (RectangleObject((x, y, width, height)), 're'), # rectangle path
        ([], 'W*'), # clip
        ]
    content.operations.append([[], "Q"]) # restore graphic state
    page[NameObject('/Contents')] = content


def _scale_pdf_page(page, factor):
    for boxname in PAGE_BOXES:
        # skip if real box does not exits (avoid fallback to other boxes)
        if not page.get(boxname):
            continue
        box = getRectangle(page, boxname, None)
        box.lowerLeft  = [float(i) * factor for i in box.lowerLeft ]
        box.upperRight = [float(i) * factor for i in box.upperRight]
        #print boxname, type(box), box
    # put transformation matrix in front of page content
    content = ContentStream(page["/Contents"].getObject(), page.pdf)
    content.operations.insert(0, [[], '%f 0 0 %f 0 0 cm' %(factor,factor)] )
    page[NameObject('/Contents')] = content


def posterize(outpdf, page, mediabox, posterbox, scale, use_ArtBox=False):
    """
    page: input page
    mediabox : size secs of the media to print on
    posterbox: size secs of the resulting poster
    scale: scale factor (to be used instead of posterbox)
    """
    if use_ArtBox:
        inbox = rectangle2box(page.artBox)
    else:
        inbox = rectangle2box(page.trimBox)
    _clip_pdf_page(page, inbox['offset_x'], inbox['offset_y'],
                   inbox['width'], inbox['height'])
    ncols, nrows, scale, rotate = decide_num_pages(inbox, mediabox,
                                                   posterbox, scale)
    mediabox = mediabox.copy()
    _scale_pdf_page(page, scale)
    if rotate:
        page.rotateClockwise(90)
        rotate_box(inbox)
        rotate_box(mediabox)
    # area to put on each page (allows for overlay of margin)
    h_step = mediabox['width']  - mediabox['offset_x']
    v_step = mediabox['height'] - mediabox['offset_y']
    
    if use_ArtBox:
        trimbox = rectangle2box(page.artBox)
    else:
        trimbox = rectangle2box(page.trimBox)
    h_pos = float(trimbox['offset_x'])
    h_max, v_max = float(trimbox['width']), float(trimbox['height'])
    for col in range(ncols):
        v_pos = float(trimbox['offset_y']) + (nrows-1) * v_step
        for row in range(nrows):
            log(17, 'Creating page with offset: %.2f %.2f' % (h_pos, v_pos))
            newpage = copyPage(page)
            # todo: if remaining area is smaller than mediaBox, add a
            # transparent fill box behind, so the real content is in
            # the lower left corner
            newpage.mediaBox = RectangleObject((h_pos, v_pos,
                                                h_pos + h_step,
                                                v_pos + v_step))
            newpage.trimBox = RectangleObject((h_pos, v_pos,
                                               min(h_max, h_pos + h_step),
                                               min(v_max, v_pos + v_step)))
            newpage.artBox = newpage.trimBox
            outpdf.addPage(newpage)
            v_pos -= v_step
        h_pos += h_step

def password_hook():
    import getpass
    return getpass.getpass()

def main(opts, infilename, outfilename, password_hook=password_hook):
    logging.basicConfig(level=20-opts.verbose, format="%(message)s")
    outpdf = PdfFileWriter()
    inpdf = PdfFileReader(open(infilename, 'rb'))

    if inpdf.isEncrypted:
        log(16, 'File is encrypted')
        # try empty password first
        if not inpdf.decrypt(''):
            if not inpdf.decrypt(password_hook()):
                raise DecryptionError("Can't decrypt PDF. Wrong Password?")

    first_page = 1
    last_page = inpdf.numPages
    if opts.first_page is not None:
        first_page = max(1, opts.first_page)
    if opts.last_page is not None:
        last_page = min(last_page, opts.last_page)

    log(18, 'Mediasize : %(units_x)sx%(units_y)s %(unit)s' % opts.media_size)
    log(17, '            %(width).2f %(height).2f dots' % opts.media_size)
    if opts.scale:
        log(18, 'Scaling by: %f' % opts.scale)
    else:
        log(18, 'Postersize: %(units_x)sx%(units_y)s %(unit)s' % opts.poster_size)
        log(17, '            %(width).2f %(height).2f dots' % opts.poster_size)

    for i in xrange(first_page-1, last_page):
        page = inpdf.getPage(i)
        log(19, '---- processing page %i -----', i+1)
        posterize(outpdf, page, opts.media_size, opts.poster_size, opts.scale,
                  opts.use_ArtBox)

    if not opts.dry_run:
        outpdf.write(open(outfilename, 'wb'))
