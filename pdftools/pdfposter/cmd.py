#!/usr/bin/env python
"""
pdftools.pdfposter.cmd - scale and tile PDF images/pages to print on multiple pages.
"""
#
# Copyright 2008-2009 by Hartmut Goebel <h.goebel@goebel-consult.de>
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

__author__ = "Hartmut Goebel <h.goebel@goebel-consult.de>"
__copyright__ = "Copyright 2008-2009 by Hartmut Goebel <h.goebel@goebel-consult.de>"
__licence__ = "GNU General Public License version 3 (GPL v3)"

from . import main, __version__, DEFAULT_MEDIASIZE, papersizes, DecryptionError
import re

# pattern for parsing user textual box spec
pat_box = re.compile(r'''
     ( (?P<width>  (\d*\.)? \d*) x                 # width "x" height
       (?P<height> (\d*\.)? \d*) )? 
     (?P<offset> \+                                # "+" offset_x "," offset_y
                 (?P<offset_x> \d+\.? | \d*\.\d+)
                 ,
                 (?P<offset_y> \d+\.? | \d*\.\d+) ) ?
     (?P<unit> [a-z][a-z0-9\-\\_]*)                # unit
     ''', re.X+re.I)

def __parse_box(option, value, parser, allow_offset=False):
    m = pat_box.match(value)
    if not m:
        raise parser.error("I don't understand your box specification %r for %s" % (value, option))
    res = m.groupdict()
    if not allow_offset and res['offset'] is not None:
        raise parser.errot('Offset not allowed in box definition for %s' % option)
    # res['offset'] is only used for error checking, remove it
    del res['offset']

    # get meassures of unit
    unit = res['unit'].lower()
    if not papersizes.has_key(unit):
        unit = [name for name in papersizes.keys()
                if name.startswith(unit)]
        if len(unit) != 1:
            parser.error('Your box spec %r for %s is not unique, give more chars.' % (res['unit'], option))
        unit = unit[0]
    unit_x, unit_y = papersizes[unit]
    res2 = {
        'width'   : float(res['width'] or 1) * unit_x,
        'height'  : float(res['height'] or 1) * unit_y,
        'offset_x': float(res['offset_x'] or 0) * unit_x,
        'offset_y': float(res['offset_y'] or 0) * unit_y,
        'unit': res['unit'],
        'units_x': res['width'] or 1,
        'units_y': res['height'] or 1,
        }
    return res2

def _parse_box(option, opt, value, parser, allow_offset=False):
    res = __parse_box(option, value, parser, allow_offset=False)
    setattr(parser.values, option.dest, res)

def run():
    import optparse
    parser = optparse.OptionParser('%prog [options] InputFile OutputFile',
                                   version=__version__)
    parser.add_option('--help-media-names', action='store_true',
                      help='List available media and disctance names')
    parser.add_option('-v', '--verbose', action='count', default=0,
                      help='Be verbose. Tell about scaling, rotation and number of pages. Can be used more than once to increase the verbosity. ')
    parser.add_option('-n', '--dry-run', action='store_true',
                      help='Show what would have been done, but do not generate files.')
    
    group = parser.add_option_group('Define Target')
    group.add_option('-m', '--media-size',
                     default=__parse_box('-m', DEFAULT_MEDIASIZE, parser),
                     action='callback', type='string', callback=_parse_box, 
                     help='Specify the size of the output media size (default: %s)' % DEFAULT_MEDIASIZE)
    group.add_option('-p', '--poster-size',
                     action='callback', type='string', callback=_parse_box, 
                     help='Specify the poster size (defaults to media size). ')
    group.add_option('-s', '--scale', type=float,
                     help='Specify a linear scaling factor to produce the poster.')

    opts, args = parser.parse_args()

    if opts.help_media_names:
        names = papersizes.keys()
        names.sort()
        parser.print_usage()
        print parser.formatter.format_heading('Avialable media and distance names')
        parser.formatter.indent()
        print parser.formatter.format_description(' '.join(names))
        raise SystemExit(0)

    if len(args) != 2:
        parser.error('requires both input and output filename')
    if opts.scale is not None and opts.poster_size is not None:
        parser.error('Only one of -p/--poster-size and -s/--scale may be given at a time.')
    if not opts.poster_size:
        opts.poster_size = opts.media_size.copy()
    if opts.scale is not None:
        opts.poster_size = None
        if opts.scale < 0.01:
            parser.error("Scale value is much to small: %s" % opts.scale)
        elif opts.scale > 1.0e6:
            parser.error("Scale value is much to big: %s" % opts.scale)

    try:
        main(opts, *args)
    except DecryptionError, e:
        raise SystemExit(str(e))


if __name__ == '__main__':
    run()
