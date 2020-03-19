
import re, os
from bisect import bisect_left
from jsonnet_docblock_parser import parser

print(os.path.abspath("jsonnet_docblock_parser/tests/resources/test.jsonnet"))
docblocks = parser.parseFile("jsonnet_docblock_parser/tests/resources/test.jsonnet")

print("printing current docbloc")
print("printing docblocks")
#for docblock in docblocks:
#  print(docblock.short_description)

print(docblocks[0].returns)
print(len(docblocks))

def count_indent(line):
  return len(line) - len(line.lstrip())


#test_comments(code)
#print(extract_comments(code))