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
    'Development Status :: 4 - Beta',
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
    ]

    # could also include long_description, etc.
)
