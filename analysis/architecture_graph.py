import networkx as nx
import plotly.graph_objects as go
from typing import List, Dict, Any

def get_module_name(p: str) -> str:
    p = p.replace("\\", "/").strip("./")
    parts = [part for part in p.split("/") if part and part not in [".", "..", "ai-code-intelligence-engine", "My PYTHON Project"]]
    if len(parts) > 1:
        return parts[0]
    return "root"

def compute_architecture_data(metadata: List[Dict[str, Any]]):
    """
    Computes graph and tabular module coupling telemetry from real metadata.
    """
    G = nx.DiGraph()
    mod_deps = {}
    node_to_mod = {m["name"]: get_module_name(m["file_path"]) for m in metadata}
    
    for m in metadata:
        current_mod = get_module_name(m["file_path"])
        if current_mod not in mod_deps:
            mod_deps[current_mod] = set()
            
        snippet = m.get("code_snippet", "")
        for other_name, other_mod in node_to_mod.items():
            if other_mod != current_mod:
                if f"{other_name}(" in snippet or f"import {other_mod}" in snippet or f"from {other_mod}" in snippet:
                    mod_deps[current_mod].add(other_mod)

    for mod, deps in mod_deps.items():
        G.add_node(mod, label=mod)
        for dep in deps:
            G.add_edge(mod, dep)

    return G

def build_architecture_graph(metadata: List[Dict[str, Any]]):
    """
    Generates an uncluttered, high-end module-level architecture graph.
    Uses circular shell topology on a clean pure white canvas matching the Reference Design Specification.
    """
    G = compute_architecture_data(metadata)

    if len(G.nodes) == 0:
        return None

    pos = nx.circular_layout(G, scale=1.2)
    
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1.5, color='rgba(99, 102, 241, 0.4)'),
        hoverinfo='none',
        mode='lines'
    )

    node_x = []
    node_y = []
    node_text = []
    node_hover = []
    node_sizes = []

    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(f"📦 {node}")
        
        in_deg = G.in_degree(node)
        out_deg = G.out_degree(node)
        node_hover.append(
            f"<b>Package Module: {node}</b><br>"
            f"📥 Inbound Calls: {in_deg}<br>"
            f"📤 Outbound Dependencies: {out_deg}<br>"
            f"🔗 Total Coupling: {in_deg + out_deg}"
        )
        node_sizes.append(max(26, min(48, 28 + (in_deg + out_deg) * 4)))

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=node_text,
        hoverinfo='text',
        hovertext=node_hover,
        textposition="top center",
        textfont=dict(family="Plus Jakarta Sans, sans-serif", size=11, color="#1e293b"),
        marker=dict(
            size=node_sizes,
            color='#4f46e5',
            line=dict(width=2, color='#f97316'),
            opacity=0.95
        )
    )

    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            paper_bgcolor='#ffffff',
            plot_bgcolor='#ffffff',
            font=dict(family="Plus Jakarta Sans, sans-serif", color="#111827"),
            showlegend=False,
            hovermode='closest',
            hoverlabel=dict(
                bgcolor="#1e293b",
                bordercolor="#f97316",
                font=dict(family="JetBrains Mono, monospace", size=11, color="#ffffff")
            ),
            margin=dict(b=25, l=25, r=25, t=25),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        )
    )
    return fig
