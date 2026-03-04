from typing import List, Dict, Any

class CodeNavigation:
    def __init__(self, metadata: List[Dict[str, Any]]):
        self.metadata = metadata

    def jump_to_definition(self, name: str) -> List[Dict[str, Any]]:
        return [item for item in self.metadata if item["name"] == name]

    def find_usages(self, name: str) -> List[Dict[str, Any]]:
        usages = []
        for item in self.metadata:
            # Simple heuristic: name appears in snippet but this isn't the definition
            if name in item["code_snippet"] and item["name"] != name:
                usages.append(item)
        return usages
