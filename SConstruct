# -*- mode: python ; coding: utf-8 -*-
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
    }

env = Environment(ENV=ENV)
env.SConsignFile()

env.Export(['env'])
env.SConscript(dirs='test')
env.SConscript(dirs='examples')

env.Command('pdfposter.1', 'pdfposter.rst',
            'python -S ./docutils-manpage-writer/rst2man.py $SOURCE $TARGET')

# create PNG projectlogo for project homepage
env.Command('projectlogo.png', 'projectlogo.svg',
            'inkscape -z -f $SOURCE -e $TARGET --export-height=100')

hires_logo = env.Command('build/icons/projectlogo-hires.png', 'projectlogo.svg',
                         'inkscape -z -f $SOURCE -e $TARGET --dpi=300')

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
