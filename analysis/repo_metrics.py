from typing import List, Dict, Any
import os

def analyze_repository(metadata: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculates various repository metrics from metadata.
    """
    if not metadata:
        return {}

    num_functions = len([m for m in metadata if m.get("type") in ["function", "method"]])
    num_classes = len([m for m in metadata if m.get("type") == "class"])
    num_files = len(set(m["file_path"] for m in metadata))
    
    modules = set()
    for m in metadata:
        p = m["file_path"].replace("\\", "/").strip("./")
        parts = [part for part in p.split("/") if part and part not in [".", ".."]]
        if len(parts) > 1:
            modules.add(parts[0])
        else:
            modules.add("root")
    
    num_modules = len(modules)
    
    # Connection analysis (heuristic)
    connections = {}
    for m in metadata:
        name = m["name"]
        snippet = m.get("code_snippet", "")
        count = 0
        for other in metadata:
            if other["name"] != name and f"{other['name']}(" in snippet:
                count += 1
        connections[name] = count
        
    total_deps = sum(connections.values())
    most_connected = sorted(connections.items(), key=lambda x: x[1], reverse=True)[:5]

    return {
        "number_of_functions": num_functions,
        "number_of_classes": num_classes,
        "number_of_files": num_files,
        "number_of_modules": num_modules,
        "total_dependencies": total_deps,
        "most_connected_nodes": most_connected
    }
