import tree_sitter_cpp
from tree_sitter import Language
from typing import List, Dict, Any
from parsers.c_parser import CParser

class CPPParser(CParser):
    def __init__(self):
        super().__init__(Language(tree_sitter_cpp.language()), "cpp")

    def parse_code(self, code: str, file_path: str) -> List[Dict[str, Any]]:
        tree = self.parser.parse(bytes(code, "utf8"))
        
        targets = {
            "function_definition": "function",
            "class_specifier": "class",
            "namespace_definition": "namespace",
            "struct_specifier": "struct"
        }
        
        results = self.traverse_tree(tree.root_node, code, file_path, targets)
        
        from utils.logger import logger
        logger.info(f"{file_path} -> extracted {len(results)} snippets")
        
        return results
