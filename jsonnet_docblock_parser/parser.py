"""The main parsing routine."""
import logging
import argparse
import sys
import re
from .common import (
    PARAM_KEYWORDS,
    RETURN_KEYWORDS,
    Docblock,
    DocblockParam,
    DocblockReturns,
    ParseError,
)
from .generator import Generator
# Set up the logger
logger = logging.getLogger("jdp")
# Use a console handler, set it to debug by default
logger_ch = logging.StreamHandler()
logger.setLevel(logging.INFO)
log_formatter = logging.Formatter(('%(levelname)s: %(asctime)s %(processName)s:%(process)d'
                                   ' %(filename)s:%(lineno)s %(module)s::%(funcName)s()'
                                   ' -- %(message)s'))
logger_ch.setFormatter(log_formatter)
logger.addHandler(logger_ch)





PATTERNS = {
    "docblock": r"\/\*\*|\*\/|.*\*",
    "tags": r"(\* \@(?P<tag>.*)\ )\s(?P<content>.*)",
    "has_tag": r".*\@\w+.*",
    "docblock_line": r".*\*\s+",
    "parse_single_line_argument": r"\@(?P<arg_name>\w+)\s(?P<type_name>\S+)\s(?P<desc>.*)",
    "check_if_optional": r".*(\(optional\)).*",
    "code": r"\s+(.*)::"
}

# @todo add long description syntaxing
# @todo add long parameter description syntaxing
def parseDocblock(lines, start_line, end_line, file) -> Docblock:
  """Parse the contents of an entire docblock.

    :param lines: An array containing all lines of a file.
    :param start_line: The key of the lines array where this docblock starts.
    :param end_line: The key of the lines array where this docblock ends.
    :return:
    """
  docblock = Docblock()
  docblock.start_line = start_line + 1
  docblock.end_line = end_line - 1
  docblock.file = file

  current_line = start_line
  abs_current_line = 0
  first_argument_found = False
  while current_line < end_line + 1:
    # Extract the description.
    if abs_current_line == 1:
      docblock.short_description = _clean_docblock_line(lines[current_line])

    if _line_has_argument(lines[current_line]):
      if not first_argument_found:
        first_argument_found = True
        docblock.long_description = _extract_long_description(lines, start_line, abs_current_line)
      # We found a "@" in this line. Check if the next line is another "@".
      param = _build_param_single_line(lines[current_line])
      #if _line_has_argument(lines[current_line+1]):
      # The next line is also a param. So no description was given for this
      # parameter.
      #  param = _build_param_single_line(lines[current_line])
      #else:
      #  param = _build_param_multi_line(lines, current_line)
      if param["type"] == DocblockParam:
        docblock.add_param(DocblockParam(
            description=param["description"],
            arg_name=param["arg_name"],
            type_name=param["type_name"],
            is_optional=param["is_optional"],
        ))
      if param["type"] == DocblockReturns:
        docblock.update_returns(DocblockReturns(
            description=param["description"],
            type_name=param["type_name"],
        ))

    current_line = current_line + 1
    abs_current_line = abs_current_line + 1

  code_line = lines[abs_current_line - 1]
  if code_line != "":
    docblock.code = code_line.strip()
  return docblock

def _extract_long_description(lines, start_line, abs_current_line):
  current_line = start_line + 1
  result = ""
  while current_line < abs_current_line:
    result = result + re.sub(PATTERNS["docblock"], "\n", lines[current_line])
    current_line = current_line + 1

  return result.lstrip()

def _build_param_single_line(line):
  pattern = re.compile(PATTERNS["parse_single_line_argument"])
  matches = pattern.search(line)
  arg_name = matches.group("arg_name")
  return_array = {
      "description": _remove_optional_from_description(matches.group("desc")),
      "type_name": matches.group("type_name"),
  }

  if arg_name in RETURN_KEYWORDS:
    return_array["type"] = DocblockReturns
  if arg_name in PARAM_KEYWORDS:
    return_array["type"] = DocblockParam
    return_array["arg_name"] = matches.group("arg_name")
    return_array["is_optional"] = _argument_is_optional(line)

  return return_array

def parseFile(file: str):
  """Parse the contents of an entire file

  :param file: The path to the jsonnet file that needs to be parsed.
  """
  if not file.endswith(".jsonnet") and not file.endswith(".libsonnet"):
    raise ParseError("Expected a .jsonnet or .libsonnet file")

  try:
    file_stream = open(file, "r")
    file_content = file_stream.read()
  except FileNotFoundError:
    logger.error("Unable to find file %s", file)
    sys.exit(1)

  lines = file_content.splitlines()
  results = {
      "docblocks": [],
      "file": file,
  }

  start_line = 0
  end_line = 0
  currently_in_docblock = False

  for i, line in enumerate(lines):
    if _is_part_of_docblock(line):
      if not currently_in_docblock:
        currently_in_docblock = True
        start_line = i
      else:
        if not _is_part_of_docblock(lines[i+1]):
          end_line = i + 2
          currently_in_docblock = False
          docblock = parseDocblock(lines, start_line, end_line, file)
          results["docblocks"].append(docblock)

  return results

def _parse_code(text):
  pattern = re.findall(PATTERNS["code"], text)
  return pattern[0] if pattern else ""

def _is_part_of_docblock(line):
  pattern = re.compile(PATTERNS["docblock"]) # Look for /* * and /** and */
  match = pattern.match(line)
  return bool(match)

def _count_indent(line):
  return len(line) - len(line.lstrip())

def _clean_docblock_line(text):
  return re.sub(PATTERNS["docblock_line"], "", text)

def _remove_optional_from_description(text):
  return text.replace('(optional) ', '')

def _line_has_argument(text):
  return _check_for(text, PATTERNS["has_tag"])

def _argument_is_optional(line):
  return _check_for(line, PATTERNS["check_if_optional"])

def _check_for(text, pattern):
  pattern = re.compile(pattern)
  match = pattern.match(text)
  return bool(match)

def main():
  logger.debug("main")

  parser = argparse.ArgumentParser(
      prog="jdp",
      description=("Jsonnet Docblock Parser. Directly executable and importable.")
  )

  parser.add_argument('-f', '--file',
                      required=True,
                      help=("The .jsonnet or .libsonnet that you want to parse."),
                      action="store")

  args = parser.parse_args()
  generator = Generator()
  results = parseFile(args.file)
  print(generator.parse_json(results))

if __name__ == '__main__':
  main()
