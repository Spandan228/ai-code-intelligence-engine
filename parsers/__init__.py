"""
AI Code Intelligence Engine - Parsers Module
Tree-sitter AST parsers for Python, JavaScript, Java, C, and C++.
"""

from .base_parser import CodeParser
BaseParser = CodeParser
from .python_parser import PythonParser
from .javascript_parser import JavaScriptParser
from .java_parser import JavaParser
from .c_parser import CParser
from .cpp_parser import CPPParser, CppParser

__all__ = [
    "CodeParser",
    "BaseParser",
    "PythonParser",
    "JavaScriptParser",
    "JavaParser",
    "CParser",
    "CPPParser",
    "CppParser",
]
