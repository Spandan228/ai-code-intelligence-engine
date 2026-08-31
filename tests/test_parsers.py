import pytest
import os
from parsers.python_parser import PythonParser

def test_extraction():
    parser = PythonParser()
    code = """
def sample_one():
    pass

class SampleClass:
    def method_one(self):
        pass
"""
    results = parser.parse_code(code, "sample.py")
    assert len(results) == 3
    names = [r["name"] for r in results]
    assert "sample_one" in names
    assert "SampleClass" in names
    assert "method_one" in names
