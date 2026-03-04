import tree_sitter_c
from tree_sitter import Language
from typing import List, Dict, Any
from parsers.base_parser import CodeParser

class CParser(CodeParser):
    def __init__(self, language: Language = None, language_id: str = "c"):
        lang = language if language else Language(tree_sitter_c.language())
        super().__init__(lang, language_id)

    def parse_code(self, code: str, file_path: str) -> List[Dict[str, Any]]:
        tree = self.parser.parse(bytes(code, "utf8"))
        
        targets = {
            "function_definition": "function",
            "struct_specifier": "struct"
        }
        
        results = self.traverse_tree(tree.root_node, code, file_path, targets)
        
        from utils.logger import logger
        logger.info(f"{file_path} -> extracted {len(results)} snippets")
        
        return results
