import ast
from radon.complexity import cc_visit
from typing import List, Dict, Any
from utils.logger import logger

class CodeSmellDetector:
    def __init__(self):
        pass

    def detect_smells(self, code: str, file_path: str) -> List[Dict[str, Any]]:
        smells = []
        
        # 1. Complexity analysis using radon
        try:
            complexity_results = cc_visit(code)
            for item in complexity_results:
                if item.complexity > 10:
                    smells.append({
                        "file": file_path,
                        "type": "High Complexity",
                        "name": item.name,
                        "value": item.complexity,
                        "suggestion": f"Refactor '{item.name}' to reduce cyclomatic complexity."
                    })
        except Exception:
            pass

        # 2. Large function detection using AST (Python) or line counting (other languages)
        found_ast = False
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    found_ast = True
                    length = (getattr(node, "end_lineno", 0) or 0) - node.lineno + 1
                    if length > 50:
                        smells.append({
                            "file": file_path,
                            "type": "Large Function",
                            "name": node.name,
                            "value": length,
                            "suggestion": f"Function '{node.name}' is {length} lines long. Consider splitting it."
                        })
        except Exception:
            pass

        if not found_ast:
            lines = code.strip().splitlines()
            if len(lines) > 50:
                smells.append({
                    "file": file_path,
                    "type": "Large Function / Block",
                    "name": file_path.split("/")[-1],
                    "value": len(lines),
                    "suggestion": f"Code block in '{file_path}' is {len(lines)} lines long. Consider breaking it up."
                })

        return smells

    def analyze_repository(self, metadata: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        all_smells = []
        # Group by file to avoid re-parsing
        file_to_code = {}
        for item in metadata:
            if item["file_path"] not in file_to_code:
                # We don't have the full file code in metadata, only snippets
                # In a real app, we'd read the file
                pass
        
        # For this demonstration, we just analyze the snippets themselves
        for item in metadata:
            smells = self.detect_smells(item["code_snippet"], item["file_path"])
            all_smells.extend(smells)
            
        return all_smells
