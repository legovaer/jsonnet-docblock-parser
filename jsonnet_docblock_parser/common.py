"""Common methods for parsing."""

import typing as T

PARAM_KEYWORDS = {
    'param',
    'parameter',
    'arg',
    'argument',
    'attribute',
    'key',
    'keyword'
}
RETURN_KEYWORDS = {
    'return',
    'returns'
}

NONE_FLAG = None

class ParseError(RuntimeError):
  """Base class for all parsing related errors."""

class DocblockParam:
  """DocstringMeta symbolizing :param metadata."""

  def __init__(self, description, arg_name, type_name, is_optional):
    """Initialize self."""
    self.description = description
    self.arg_name = arg_name
    self.type_name = type_name
    self.is_optional = is_optional

  def __str__(self):
    # Override to print a readable string presentation of your object
    # below is a dynamic way of doing this without explicity constructing the string manually
    return ', '.join(['{key}={value}'.format(key=key, value=self.__dict__.get(key)) for key in self.__dict__]) # pylint: disable=line-too-long

  def get_description(self):
    """Get the description of this parameter"""
    return self.description


class DocblockReturns:
  """'DocstringMeta symbolizing @returns metadata.'"""

  def __init__(self, description, type_name):
    """Initialize self."""
    self.description = description
    self.type_name = type_name

  def __str__(self):
    # Override to print a readable string presentation of your object
    # below is a dynamic way of doing this without explicity constructing the string manually
    return ', '.join(['{key}={value}'.format(key=key, value=self.__dict__.get(key)) for key in self.__dict__]) # pylint: disable=line-too-long

  def get_type_name(self):
    """Get the type name of the return value."""
    return self.type_name

  def get_description(self):
    """Get the description of the return value."""
    return self.description

class Docblock:
  """Docblock object representation."""

  def __init__(self):
    """Initialize self."""
    self.short_description = None
    self.long_description = None
    self.code = None
    self.params = []
    self.returns = None
    self.start_line = None
    self.end_line = None

  def add_param(self, param):
    """Add a parameter to the metadata of this docblock."""
    self.params.append(param)

  def update_returns(self, param):
    """Update the @return metadata of this docblock."""
    self.returns = param

  def get_params(self) -> T.List[DocblockParam]:
    """Get all the parameters that are found in this docblock."""
    return self.params

  def render(self):
    """Render the docblock element."""

    result = {
        'short_description': self.short_description,
        'long_description': self.long_description,
        'code': self.code,
        'params': [],
        'start_line': self.start_line,
        'end_line': self.end_line,
    }
    for param in self.params:
      data = {
          'description': param.description,
          'type_name': param.type_name,
          'is_optional': param.is_optional
      }
      result['params'].append(data)

    if self.returns != NONE_FLAG:
      result['returns'] = {
          'description': self.returns.description,
          'type_name': self.returns.type_name
      }

    return result

  def __str__(self):
    # Override to print a readable string presentation of your object
    # below is a dynamic way of doing this without explicity constructing the string manually
    return ', '.join(['{key}={value}'.format(key=key, value=self.__dict__.get(key)) for key in self.__dict__]) # pylint: disable=line-too-long
