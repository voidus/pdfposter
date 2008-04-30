
import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages

setup(
    name = "pdfposter",
    version = "0.2",
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
