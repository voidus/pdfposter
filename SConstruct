# -*- mode: python ; coding: utf-8 -*-
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
#
# Build requirements
# - docutils
# - inkscape
#
# For building tests
# - pdf2ps (comes with ghostscript)
# - poster 
#
# For building examles
# Build requirements
# - ImageMagick
#

import os

ENV = {
    'PYTHONPATH': os.environ['PYTHONPATH'],
    'PATH': os.environ['PATH'],
    }

env = Environment(ENV=ENV)
env.SConsignFile()

env.Export(['env'])
env.SConscript(dirs='test')
env.SConscript(dirs='examples')

env.Command(['docs/pdfposter.1', 'docs/pdfposter.html'],
            'pdfposter.rst',
            'python setup.py build_docs')

# create PNG projectlogo for project homepage
env.Command('projectlogo.png', 'projectlogo.svg',
            'inkscape -z -f $SOURCE -e $TARGET --export-height=100')

hires_logo = env.Command('build/icons/projectlogo-hires.png', 'projectlogo.svg',
                         'inkscape -z -f $SOURCE -e $TARGET')

icon_parts = [
    env.Command('build/icons/project-${WIDTH}x${HEIGHT}.pnm', hires_logo,
                'pngtopnm $SOURCE ' \
                '| pnmscale -width=$WIDTH -height=$HEIGHT ' \
                '| ppmquant 256 > $TARGET',
                WIDTH=w, HEIGHT=w)
    for w in (16, 32, 48)
    ]

env.Command('projectlogo.ico', icon_parts,
            'ppmtowinicon $SOURCES > $TARGET')
