import networkx as nx
import plotly.graph_objects as go
import os
from typing import List, Dict, Any

def build_architecture_graph(metadata: List[Dict[str, Any]]):
    """
    Generates a module-level architecture graph.
    Nodes represent directories/packages, edges represent cross-module calls.
    """
    G = nx.DiGraph()
    
    # Identify modules (top-level folders under project root or based on path)
    def get_module(p):
        parts = p.split(os.sep)
        # Try to find a reasonable module name
        for part in parts:
            if part not in [".", "..", "ai-code-intelligence-engine", "My PYTHON Project"]:
                return part
        return "root"

    mod_deps = {} # module -> set of modules it depends on
    
    # Extract dependencies based on snippet analysis
    node_to_mod = {m["name"]: get_module(m["file_path"]) for m in metadata}
    
    for m in metadata:
        current_mod = get_module(m["file_path"])
        if current_mod not in mod_deps:
            mod_deps[current_mod] = set()
            
        snippet = m.get("code_snippet", "")
        for other_name, other_mod in node_to_mod.items():
            if other_mod != current_mod:
                if f"{other_name}(" in snippet or f"import {other_mod}" in snippet:
                    mod_deps[current_mod].add(other_mod)

    for mod, deps in mod_deps.items():
        G.add_node(mod, label=mod)
        for dep in deps:
            G.add_edge(mod, dep)

    if len(G.nodes) == 0:
        return None

    pos = nx.spring_layout(G, k=1.5)
    
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=2, color='#555'),
        hoverinfo='none',
        mode='lines'
    )

    node_x = []
    node_y = []
    node_text = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=node_text,
        textposition="top center",
        marker=dict(size=25, color='lightblue', line_width=2)
    )

    fig = go.Figure(data=[edge_trace, node_trace],
                 layout=go.Layout(
                    title='Project Architecture Overview (Modules)',
                    showlegend=False,
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )
    return fig
