import networkx as nx
import plotly.graph_objects as go
from typing import List, Dict, Any

def build_focused_graph(target_name: str, metadata: List[Dict[str, Any]]):
    """
    Generates a dependency graph centered around a specific target name.
    Includes the target, nodes it calls, and nodes that call it.
    """
    G = nx.DiGraph()
    
    # First pass: find all nodes and their basic info
    node_map = {m["name"]: m for m in metadata}
    
    # Case-insensitive partial matching
    target_key = None
    target_lower = target_name.lower()

    for name in node_map.keys():
        if target_lower in name.lower():
            target_key = name
            break

    if target_key is None:
        return None

    target_name = target_key

    # Identify target and its immediate neighbors
    relevant_nodes = {target_name}
    
    # We need to find connections without modifying graph_builder.py
    # Heuristic: check if target_name is in code_snippet of others (callers)
    # or if others names are in target's snippet (callees)
    
    target_meta = node_map[target_name]
    target_snippet = target_meta.get("code_snippet", "")
    
    # Find Callees (nodes target calls)
    for name, meta in node_map.items():
        if name == target_name: continue
        if f"{name}(" in target_snippet or f" {name}" in target_snippet:
            relevant_nodes.add(name)
            G.add_edge(target_name, name)
            
    # Find Callers (nodes that call target)
    for name, meta in node_map.items():
        if name == target_name: continue
        snippet = meta.get("code_snippet", "")
        if f"{target_name}(" in snippet or f" {target_name}" in snippet:
            relevant_nodes.add(name)
            G.add_edge(name, target_name)

    # Add nodes with labels
    for node in relevant_nodes:
        G.add_node(node, label=node)

    if len(G.nodes) == 0:
        G.add_node(target_name, label=target_name)

    pos = nx.spring_layout(G, k=1.0)
    
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color='#888'),
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
        node_text.append(G.nodes[node]['label'])

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=node_text,
        textposition="top center",
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='Viridis',
            size=15,
            color=[1 if n == target_name else 0 for n in G.nodes()],
            colorbar=dict(
                thickness=15,
                title=dict(text="Node Type"),
                xanchor="left",
                tickvals=[0, 1],
                ticktext=['Neighbor', 'Target']
            )
        )
    )

    fig = go.Figure(data=[edge_trace, node_trace],
                 layout=go.Layout(
                    title=f'Focused Graph: {target_name}',
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )
    if isinstance(fig, str):
        import json
        fig = go.Figure(json.loads(fig))
    return fig
