#!/usr/bin/env python
#
# Copyright 2012 by Hartmut Goebel <h.goebel@goebel-consult.de>
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
__copyright__ = "Copyright 2012 by Hartmut Goebel <h.goebel@goebel-consult.de>"
__licence__ = "GNU General Public License version 3 (GPL v3)"

import unittest
from pdftools.pdfposter.cmd import __parse_box as parse_box

class ArgParserError(Exception): pass

class PseudoParser:
    def error(self, msg):
        raise ArgParserError(msg)

class TextBoxes(unittest.TestCase):

    def _parse_box(self, value, allow_offset=False):
        return parse_box('--poster', value, PseudoParser(), allow_offset)

    def assertBoxValue(self, box, k, v):
        self.assertEqual(box[k], v, 'box[%r] == %r != %r' % (k, box[k], v))

    def test_papersize_abbreviation(self):
        box = self._parse_box('1x1let')
        self.assertBoxValue(box, 'unit', 'letter')
        box = self._parse_box('1x1envdin')
        self.assertBoxValue(box, 'unit', 'envdinlang')

    def test_ambiguous_papersize_abbreviation_raises(self):
        self.assertRaisesRegexp(
            ArgParserError, "papersize name .* is not unique",
            self._parse_box, '1x1a')

    def test_unknown_papersize_raises(self):
        self.assertRaisesRegexp(
            ArgParserError, "I don't understand your papersize name",
            self._parse_box, '1x2yyy')
        self.assertRaisesRegexp(
            ArgParserError, "I don't understand your papersize name",
            self._parse_box, '1x2xxx')

    def test_wrong_box_definition_raises(self):
        self.assertRaisesRegexp(
            ArgParserError, "I don't understand your box specification",
            self._parse_box, '2yyy')
        self.assertRaisesRegexp(
            ArgParserError, "I don't understand your box specification",
            self._parse_box, '2xxx')


if __name__ == '__main__':
    unittest.main()
