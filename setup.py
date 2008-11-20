"""
``Pdfposter`` can be used to create a large poster by building it from
multple pages and/or printing it on large media. It expects as input a
PDF file, normally printing on a single page. The output is again a
PDF file, maybe containing multiple pages together building the
poster.
The input page will be scaled to obtain the desired size.

This is much like ``poster`` does for Postscript files, but working
with PDF. Since sometimes poster does not like your files converted
from PDF. :-) Indeed ``pdfposter`` was inspired by ``poster``.

For more information please refere to the manpage or visit
the `project homepage <http://pdfposter.origo.ethz.ch/>`_.
"""

import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages
additional_keywords ={}

try:
    import py2exe
except ImportError:
    py2exe = None

if py2exe:
    resources = {
        #'other_resources': [(u"VERSIONTAG",1,myrevisionstring)],
        'icon_resources' : [(1,'projectlogo.ico')]
        }
    additional_keywords.update({
        'windows': [],
        'console': [dict(script='pdfposter', **resources)],
        'zipfile': None,
        })

setup(
    name = "pdfposter",
    version = "0.4.4",
    scripts = ['pdfposter'],
    install_requires = ['pyPdf>1.10'],

    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst'],
        # And include any *.msg files found in the 'hello' package, too:
        'hello': ['*.msg'],
        },

    # metadata for upload to PyPI
    author = "Hartmut Goebel",
    author_email = "h.goebel@goebel-consult.de",
    description = "Scale and tile PDF images/pages to print on multiple pages.",
    long_description = __doc__,
    license = "GPL 3.0",
    keywords = "pdf poster",
    url          = "http://pdfposter.origo.ethz.ch/",
    download_url = "http://pdfposter.origo.ethz.ch/download",
    classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Intended Audience :: End Users/Desktop',
    'Intended Audience :: System Administrators',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Printing',
    'Topic :: Utilities',
    ],


    # these are for easy_install (used by bdist_*)
    zip_safe = True,
    entry_points = {
        "console_scripts": [
            "pdfposter = pdftools.pdfposter.cmd:run",
        ],
    },
    # these are for py2exe
    options = {
        # bundle_files 1: bundle everything, including the Python interpreter 
        # bundle_files 2: bundle everything but the Python interpreter
        # bundle_files 3: don't bundle
       "py2exe":{"optimize": 2,
                 "bundle_files": 1,
                 "includes": [],
                }
        },
    **kw
)

import glob, os
for fn in glob.glob('*.egg-link'): os.remove(fn)
