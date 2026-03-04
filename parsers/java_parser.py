import tree_sitter_java
from tree_sitter import Language
from typing import List, Dict, Any
from parsers.base_parser import CodeParser

class JavaParser(CodeParser):
    def __init__(self):
        super().__init__(Language(tree_sitter_java.language()), "java")

    def parse_code(self, code: str, file_path: str) -> List[Dict[str, Any]]:
        tree = self.parser.parse(bytes(code, "utf8"))
        
        targets = {
            "class_declaration": "class",
            "method_declaration": "method",
            "constructor_declaration": "method"
        }
        
        results = self.traverse_tree(tree.root_node, code, file_path, targets)
        
        from utils.logger import logger
        logger.info(f"{file_path} -> extracted {len(results)} snippets")
        
        return results
