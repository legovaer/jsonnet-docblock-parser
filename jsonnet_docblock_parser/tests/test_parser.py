# -*- coding: utf-8 -*-
"""Unit tests for the parser component"""

import pytest

from jsonnet_docblock_parser import parseFile, ParseError

TRUE_FLAG = True
FALSE_FLAG = False

TEST_FILE = "jsonnet_docblock_parser/tests/resources/test.jsonnet"

def test_file_loader():
  """Tests if invalid files cannot be loaded"""
  with pytest.raises(ParseError):
    parseFile("file_has_no_jsonnet_extension")

def test_test_parse_file():
  """Tests the parseFile method of the parser object."""
  docblocks = parseFile(TEST_FILE)
  assert len(docblocks) == 1
  assert len(docblocks[0].params) == 2
  assert docblocks[0].short_description == "Returns whether the string a is prefixed by the string b." # pylint: disable=line-too-long
  assert docblocks[0].long_description == "Returns whether the string a is prefixed by the string b.\n\n Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut venenatis ex tellus, ac\n consectetur libero pretium in. Donec vehicula est nec odio cursus, non condimentum\n est cursus. Integer dui sapien, tincidunt non velit non, bibendum facilisis mi. Morbi" # pylint: disable=line-too-long
  assert docblocks[0].code == "startsWith(a, b):"
  assert docblocks[0].start_line == 2
  assert docblocks[0].end_line == 12
  assert docblocks[0].file == TEST_FILE
  assert docblocks[0].returns.description == "true if string a is prefixed by the string b or false otherwise." # pylint: disable=line-too-long
  assert docblocks[0].returns.type_name == "bool"
  assert docblocks[0].params[0].description == "The input string."
  assert docblocks[0].params[0].arg_name == "param"
  assert docblocks[0].params[0].type_name == "a"
  assert docblocks[0].params[0].is_optional == FALSE_FLAG
  assert docblocks[0].params[1].description == "The prefix."
  assert docblocks[0].params[1].arg_name == "param"
  assert docblocks[0].params[1].type_name == "b"
  assert docblocks[0].params[1].is_optional == TRUE_FLAG
