from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from tree_sitter import Language, Parser
from typing import List, Dict, Any, Optional

class CodeParser(ABC):
    def __init__(self, language: Language, language_id: str):
        self.language_id = language_id
        self.language = language
        self.parser = Parser(language)

    @abstractmethod
    def parse_code(self, code: str, file_path: str) -> List[Dict[str, Any]]:
        """Parses code and returns a list of metadata for snippets (functions, classes, etc.)"""
        pass

    def traverse_tree(self, node, code: str, file_path: str, targets: Dict[str, str]) -> List[Dict[str, Any]]:
        results = []
        
        if node.type in targets:
            name_node = node.child_by_field_name("name")
            name = name_node.text.decode("utf8") if name_node else "anonymous"
            
            snippet = self.extract_snippet(code, node)
            results.append({
                "file_path": file_path,
                "language": self.language_id,
                "type": targets[node.type],
                "name": name,
                "code_snippet": snippet,
                "start_line": node.start_point[0] + 1
            })
        
        for child in node.children:
            results.extend(self.traverse_tree(child, code, file_path, targets))
            
        return results

    def extract_snippet(self, code: str, node) -> str:
        lines = code.splitlines()
        start_line = node.start_point[0]
        end_line = node.end_point[0]
        # Safety check for multi-line snippets
        if end_line >= len(lines):
            end_line = len(lines) - 1
        return "\n".join(lines[start_line : end_line + 1])
