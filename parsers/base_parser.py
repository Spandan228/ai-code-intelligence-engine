from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from tree_sitter import Language, Parser

class CodeParser(ABC):
    def __init__(self, language: Language, language_id: str):
        self.language_id = language_id
        self.language = language
        self.parser = Parser(language)

    @abstractmethod
    def parse_code(self, code: str, file_path: str) -> List[Dict[str, Any]]:
        """Parses code and returns a list of metadata for snippets (functions, classes, etc.)"""
        pass

    def extract_name(self, node) -> str:
        name_node = node.child_by_field_name("name")
        if name_node and hasattr(name_node, "text"):
            return name_node.text.decode("utf8")
        
        # In C / C++, the function name is located in the declarator hierarchy
        if node.type == "function_definition":
            declarator = node.child_by_field_name("declarator")
            while declarator and declarator.type in ("function_declarator", "pointer_declarator", "reference_declarator"):
                child_dec = declarator.child_by_field_name("declarator")
                if child_dec:
                    declarator = child_dec
                else:
                    for c in declarator.children:
                        if c.type in ("identifier", "field_identifier"):
                            declarator = c
                            break
                    else:
                        declarator = declarator.children[0] if declarator.children else None
            if declarator and hasattr(declarator, "text"):
                return declarator.text.decode("utf8")

        # In JS, arrow functions assigned to variables
        if node.type == "arrow_function" and node.parent and node.parent.type == "variable_declarator":
            var_name = node.parent.child_by_field_name("name")
            if var_name and hasattr(var_name, "text"):
                return var_name.text.decode("utf8")

        return "anonymous"

    def traverse_tree(self, node, code: str, file_path: str, targets: Dict[str, str]) -> List[Dict[str, Any]]:
        results = []
        
        if node.type in targets:
            # For C/C++ struct/class specifiers, ignore type references without body
            if node.type in ("struct_specifier", "class_specifier") and not node.child_by_field_name("body"):
                pass
            else:
                name = self.extract_name(node)
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

