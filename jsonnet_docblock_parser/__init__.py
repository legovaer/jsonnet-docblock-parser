"""Parse docblock as per C++ notation."""

from .common import (
    Docblock,
    DocblockParam,
    DocblockReturns,
    ParseError,
)

from .parser import parseFile

__all__ = [
    "parseFile",
    "Docblock",
    "DocblockParam",
    "DocblockReturns",
    "ParseError",
]
