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
the `project homepage <http://pythonhosted.org/pdftools.pdfposter/>`_.
"""

import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages
additional_keywords ={}

try:
    import py2exe
except ImportError:
    py2exe = None

from distutils.core import Command
from distutils import log
import os

class build_docs(Command):
    description = "build documentation from rst-files"
    user_options=[]

    def initialize_options (self): pass
    def finalize_options (self):
        self.docpages = DOCPAGES
        
    def run(self):
        substitutions = ('.. |VERSION| replace:: '
                         + self.distribution.get_version())
        for writer, rstfilename, outfilename in self.docpages:
            distutils.dir_util.mkpath(os.path.dirname(outfilename))
            log.info("creating %s page %s", writer, outfilename)
            if not self.dry_run:
                try:
                    rsttext = open(rstfilename).read()
                except IOError, e:
                    sys.exit(e)
                rsttext = '\n'.join((substitutions, rsttext))
                # docutils.core does not offer easy reading from a
                # string into a file, so we need to do it ourself :-(
                doc = docutils.core.publish_string(source=rsttext,
                                                   source_path=rstfilename,
                                                   writer_name=writer)
                try:
                    rsttext = open(outfilename, 'w').write(doc)
                except IOError, e:
                    sys.exit(e)

cmdclass = {}

try:
    import docutils.core
    import docutils.io
    import docutils.writers.manpage
    import distutils.command.build
    distutils.command.build.build.sub_commands.append(('build_docs', None))
    cmdclass['build_docs'] = build_docs
except ImportError:
    log.warn("docutils not installed, can not build man pages. "
             "Using pre-build ones.")

DOCPAGES = (
    ('manpage', 'pdfposter.rst', 'docs/pdfposter.1'),
    ('html', 'pdfposter.rst', 'docs/pdfposter.html'),
    )

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
    cmdclass=cmdclass,
    name = "pdftools.pdfposter",
    version = "0.6.1dev",
    #scripts = ['pdfposter'],
    install_requires = ['PyPdf2'],

    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['pdftools'],

    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst'],
        # And include any *.msg files found in the 'hello' package, too:
        'hello': ['*.msg'],
        },

    # metadata for upload to PyPI
    author = "Hartmut Goebel",
    author_email = "h.goebel@crazy-compilers.com",
    description = "Scale and tile PDF images/pages to print on multiple pages.",
    long_description = __doc__,
    license = "GPL 3.0",
    keywords = "pdf poster",
    url          = "http://pythonhosted.org/pdftools.pdfposter/",
    download_url = "http://pypi.python.org/pypi/pdftools.pdfposter/",
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
    **additional_keywords
)
