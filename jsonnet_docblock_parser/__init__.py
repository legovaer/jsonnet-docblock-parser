"""Parse docblock as per C++ notation."""

from .common import (
    Docblock,
    DocblockParam,
    DocblockReturns,
    ParseError,
)

from .parser import parseFile

from .generator import Generator

__all__ = [
    "parseFile",
    "Docblock",
    "DocblockParam",
    "DocblockReturns",
    "ParseError",
    "Generator"
]
