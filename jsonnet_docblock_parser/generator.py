"""A generator that is able to render output."""

import json

class Generator:
  """The generator class that will generate the output."""

  def __init__(self) -> None:
    self.results = []

  def parse_json(self, results):
    """Parse the given results in JSON format."""
    self.results = results
    output = []

    # This results array contains all docblocks found in the file.
    for docblock in results:
      output.append(docblock.render())

    return json.dumps(output, indent=4)

  def get_results(self):
    """Get the results that are stored in this generator."""
    return self.results
