#!/usr/bin/env python
#
# Copyright 2012-2013 by Hartmut Goebel <h.goebel@crazy-compilers.com>
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

__author__ = "Hartmut Goebel <h.goebel@crazy-compilers.com>"
__copyright__ = "Copyright 2012-2013 by Hartmut Goebel <h.goebel@crazy-compilers.com>"
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

    def test_disallowed_offset_raises(self):
        self.assertRaisesRegexp(
            ArgParserError, "Offset not allowed in box definition",
            self._parse_box, '1x1+10,10a4')
        # not even if zero
        self.assertRaisesRegexp(
            ArgParserError, "Offset not allowed in box definition",
            self._parse_box, '1x1+0,0a4')

    def test_missing_offset_raises(self):
        self.assertRaisesRegexp(
            ArgParserError, "I don't understand your box specification",
            self._parse_box, '1x1+a4')

    def test_allowed_offset_does_not_raise(self):
        self._parse_box('1x1+10,10a4', allow_offset=True)
        self._parse_box('1x1+0,0a4', allow_offset=True)

    def test_some_standard_papersizes(self):
        box = self._parse_box('1x1a4')
        for k, v in (
            ('width', 595),
            ('height', 842),
            ('offset_x', 0),
            ('offset_y', 0),
            ('unit', 'a4'),
            ('units_x', 1),
            ('units_y', 1)):
            self.assertBoxValue(box, k, v)
        box = self._parse_box('a4')
        for k, v in (
            ('width', 595),
            ('height', 842),
            ('offset_x', 0),
            ('offset_y', 0),
            ('unit', 'a4'),
            ('units_x', 1),
            ('units_y', 1)):
            self.assertBoxValue(box, k, v)
        box = self._parse_box('1x1tabloid')
        for k, v in (
            ('width', 792),
            ('height', 1224),
            ('offset_x', 0),
            ('offset_y', 0),
            ('unit', 'tabloid'),
            ('units_x', 1),
            ('units_y', 1)):
            self.assertBoxValue(box, k, v)

    def test_multiplier(self):
        box = self._parse_box('2x2a4')
        for k, v in (
            ('width', 2 * 595),
            ('height', 2 * 842),
            ('offset_x', 0),
            ('offset_y', 0),
            ('unit', 'a4'),
            ('units_x', 2),
            ('units_y', 2)):
            self.assertBoxValue(box, k, v)
        box = self._parse_box('7.2x3.5a4')
        for k, v in (
            ('width', 7.2 * 595),
            ('height', 3.5 * 842),
            ('offset_x', 0),
            ('offset_y', 0),
            ('unit', 'a4'),
            ('units_x', 7.2),
            ('units_y', 3.5)):
            self.assertBoxValue(box, k, v)

    def test_complex_box_specification(self):
        box = self._parse_box('7.2x3.5+1.5,0.3a4', allow_offset=True)
        for k, v in (
            ('width', 7.2 * 595),
            ('height', 3.5 * 842),
            ('offset_x', 1.5 * 595),
            ('offset_y', 0.3 * 842),
            ('unit', 'a4'),
            ('units_x', 7.2),
            ('units_y', 3.5)):
            self.assertBoxValue(box, k, v)


if __name__ == '__main__':
    unittest.main()
