from typing import List, Dict, Any
from search.semantic_search import SemanticSearch

class CodeExplainer:
    def __init__(self, search_engine: SemanticSearch):
        self.search_engine = search_engine

    def explain_code(self, snippet: str) -> str:
        """
        Retrieves context and generates a structured explanation for the code snippet.
        """
        # Step 1: Find related code using semantic search
        results = self.search_engine.search(snippet, top_k=3)
        
        # Step 2: Extract context
        context_names = [r["name"] for r in results]
        context_files = list(set([r["file_path"] for r in results]))
        
        # Heuristic explanation generator
        # In a production app, we would call an LLM here with the snippet and retrieved context.
        # For this implementation, we provide a sophisticated heuristic-based description.
        
        explanation = "### 🤖 AI Code Explanation\n\n"
        
        if "class " in snippet or "struct " in snippet or "interface " in snippet:
            explanation += "This block defines a **class structure** or type abstraction that encapsulates data and behavior. "
        elif "def " in snippet or "function" in snippet or "method" in snippet or "=>" in snippet:
            explanation += "This code block defines a **functional entity** responsible for specific execution logic. "
        else:
            explanation += "This is a **code fragment** representing a partial logic flow. "
            
        context_str = ", ".join(context_names[:5]) if context_names else "None (isolated snippet)"
        files_str = ", ".join(context_files[:3]) if context_files else "None"
        explanation += f"\n\n**Semantic Context:**\n"
        explanation += f"- Relates to existing entities: `{context_str}`\n"
        explanation += f"- Contextual files found: `{files_str}`\n\n"
        
        # Dynamic purpose description based on keywords
        purpose = "The snippet seems to handle "
        keywords_found = []
        if any(w in snippet.lower() for w in ["login", "auth", "cred", "user"]): keywords_found.append("authentication")
        if any(w in snippet.lower() for w in ["db", "db.", "connect", "sql", "query"]): keywords_found.append("database operations")
        if any(w in snippet.lower() for w in ["plot", "graph", "fig", "chart"]): keywords_found.append("data visualization")
        if any(w in snippet.lower() for w in ["index", "search", "vector", "embed"]): keywords_found.append("information retrieval")
        
        if keywords_found:
            purpose += " and ".join(keywords_found) + "."
        else:
            purpose += "general application logic based on the retrieved context."
            
        explanation += f"**Purpose:**\n{purpose}\n\n"
        explanation += "> [!TIP]\n"
        explanation += "> To improve this code, ensure robust error handling and type hinting for the detected primary purpose."
        
        return explanation
