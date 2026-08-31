from typing import List, Dict, Any
from indexer.language_detector import LanguageDetector
from parsers.python_parser import PythonParser
from parsers.java_parser import JavaParser
from parsers.javascript_parser import JavaScriptParser
from parsers.c_parser import CParser
from parsers.cpp_parser import CPPParser

class CodeParserOrchestrator:
    def __init__(self):
        self.parsers = {
            "python": PythonParser(),
            "java": JavaParser(),
            "javascript": JavaScriptParser(),
            "c": CParser(),
            "cpp": CPPParser()
        }

    def parse_file(self, file_path: str) -> List[Dict[str, Any]]:
        language = LanguageDetector.get_language(file_path)
        if language == "unknown" or language not in self.parsers:
            return []

        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                code = f.read()
            return self.parsers[language].parse_code(code, file_path)
        except Exception as e:
            from utils.logger import logger
            logger.error(f"Error parsing file {file_path}: {e}")
            return []
