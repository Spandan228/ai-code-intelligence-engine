import networkx as nx
import plotly.graph_objects as go
import math
from typing import List, Dict, Any

def build_focused_graph(target_name: str, metadata: List[Dict[str, Any]]):
    """
    Generates a high-clarity focused neighborhood graph around a target symbol.
    Uses radial concentric positioning: Target in center (0,0), callers on left, callees on right.
    Styled with Reference Design System tokens (pure white surface, gold target, cyan callers, violet callees).
    """
    node_map = {m["name"]: m for m in metadata}
    
    # Case-insensitive partial matching for target entity
    target_key = None
    target_lower = target_name.lower()

    for name in node_map.keys():
        if target_lower in name.lower():
            target_key = name
            break

    if target_key is None:
        return None

    target_name = target_key
    target_meta = node_map[target_name]
    target_snippet = target_meta.get("code_snippet", "")
    
    callers = set()
    callees = set()
    
    # Find Callees (functions target calls)
    for name, meta in node_map.items():
        if name == target_name: continue
        if f"{name}(" in target_snippet or f" {name}" in target_snippet:
            callees.add(name)
            
    # Find Callers (functions that call target)
    for name, meta in node_map.items():
        if name == target_name: continue
        snippet = meta.get("code_snippet", "")
        if f"{target_name}(" in snippet or f" {target_name}" in snippet:
            callers.add(name)

    G = nx.DiGraph()
    G.add_node(target_name, role="target", label=target_name)
    
    for c in callers:
        G.add_node(c, role="caller", label=c)
        G.add_edge(c, target_name)
        
    for c in callees:
        G.add_node(c, role="callee", label=c)
        G.add_edge(target_name, c)

    pos = {}
    pos[target_name] = (0.0, 0.0)

    # Position callers evenly on left semicircle
    callers_list = sorted(list(callers))
    n_callers = len(callers_list)
    for i, c in enumerate(callers_list):
        angle = math.pi/2 + (math.pi * (i + 0.5) / max(n_callers, 1))
        pos[c] = (-1.5 + 0.3 * math.cos(angle), 1.2 * math.sin(angle))

    # Position callees evenly on right semicircle
    callees_list = sorted(list(callees))
    n_callees = len(callees_list)
    for i, c in enumerate(callees_list):
        angle = -math.pi/2 + (math.pi * (i + 0.5) / max(n_callees, 1))
        pos[c] = (1.5 + 0.3 * math.cos(angle), 1.2 * math.sin(angle))

    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1.5, color='rgba(148, 163, 184, 0.5)'),
        hoverinfo='none',
        mode='lines'
    )

    node_x = []
    node_y = []
    node_text = []
    node_hover = []
    node_colors = []
    node_sizes = []

    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        role = G.nodes[node].get("role", "neighbor")
        label = G.nodes[node]["label"]
        
        if role == "target":
            node_text.append(f"⭐ {label}")
            node_hover.append(f"<b>[Target Entity]</b><br>Symbol: {label}<br>Inbound Callers: {n_callers}<br>Outbound Callees: {n_callees}")
            node_colors.append("#f97316")
            node_sizes.append(34)
        elif role == "caller":
            node_text.append(label)
            node_hover.append(f"<b>[Inbound Caller]</b><br>Calls target '{target_name}'")
            node_colors.append("#0284c7")
            node_sizes.append(22)
        else: # callee
            node_text.append(label)
            node_hover.append(f"<b>[Outbound Callee]</b><br>Invoked by target '{target_name}'")
            node_colors.append("#8b5cf6")
            node_sizes.append(22)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=node_text,
        textposition="top center",
        hoverinfo='text',
        hovertext=node_hover,
        textfont=dict(family="Plus Jakarta Sans, sans-serif", size=10, color="#1e293b"),
        marker=dict(
            size=node_sizes,
            color=node_colors,
            line=dict(width=2, color='#ffffff')
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
