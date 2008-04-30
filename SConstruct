# -*- mode: python ; coding: utf-8 -*-
#
# Build requirements
# - docutils
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
    
env.Export(['env'])
env.SConscript(dirs='test')
