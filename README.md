# Jsonnet Docblock Parser

JDP is a simple, powerfull jsonnet docblock parser that returns a JSON representation to work with.

[![Build Status](https://travis-ci.com/legovaer/jsonnet-docblock-parser.svg?branch=master)](https://travis-ci.com/legovaer/jsonnet-docblock-parser)
[![PyPI status](https://img.shields.io/pypi/status/jsonnet_docblock_parser.svg)](https://pypi.python.org/pypi/jsonnet_docblock_parser/)
[![PyPI version shields.io](https://img.shields.io/pypi/v/jsonnet_docblock_parser.svg)](https://pypi.python.org/pypi/jsonnet_docblock_parser/)
[![PyPI license](https://img.shields.io/pypi/l/jsonnet_docblock_parser.svg)](https://pypi.python.org/pypi/jsonnet_docblock_parser/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/jsonnet_docblock_parser.svg)](https://pypi.python.org/pypi/jsonnet_docblock_parser/)

This parser will extract docblocks from your `.jsonnet` or `.libsonnet` files. This package
includes a generator that allows you to output the parsed information into JSON format.

The parser assumes that the documentation inside these files is written in a syntax that is 
similar to JavaScript, Java and many C++ scripts:

```
{
  /**
   * Returns whether the string a is prefixed by the string b.
   *
   * @param a The input string.
   * @param b The prefix.
   * @return true if string a is prefixed by the string b or false otherwise.
   */
  startsWith(a, b):
    if std.length(a) < std.length(b) then
      false
    else
      std.substr(a, 0, std.length(b)) == b,
}
```

## Installation

You can install the tool via pip:

```bash
pip install jsonnet-docblock-parser
```

## Module Usage

```python
#!/usr/bin/env python
# encoding: utf-8

from jsonnet_docblock_parser import parseFile, Generator

# Load a jsonnet or libsonnet file.
TEST_FILE = "some.jsonnet"

# Parse the file.
docblocks = parseFile(TEST_FILE)

# Load the generator.
generator = Generator()

# Parse Json based on the results.
json = generator.parse_json(results)

# Print the json
print(json)
```

## CLI Usage

```bash
jdp --file some.jsonnet
```

## Development

### Testing

```bash
pytest
```

### PyLint

```bash
pylint jsonnet_docblock_parser
```

### Deploying to PyPi

```bash
python3 setup.py sdist
twine upload dist/*
```

## License

The MIT License (MIT). Please see [License File](LICENSE.md) for more information.