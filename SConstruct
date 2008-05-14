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

import os

ENV = {
    'PYTHONPATH': os.environ['PYTHONPATH'],
    }

env = Environment(ENV=ENV)
env.SConsignFile()

env.Command('pdfposter.1', 'pdfposter.rst',
            'python -S ./docutils-manpage-writer/rst2man.py $SOURCE $TARGET')

# create PNG projectlogo for project homepage
env.Command('projectlogo.png', 'projectlogo.svg',
            'inkscape -z -f $SOURCE -e $TARGET --export-height=100')

env.Export(['env'])
env.SConscript(dirs='test')
