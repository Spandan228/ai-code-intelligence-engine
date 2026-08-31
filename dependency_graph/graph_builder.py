import networkx as nx
import plotly.graph_objects as go
from typing import List, Dict, Any
import math

class GraphBuilder:
    def __init__(self):
        self.graph = nx.DiGraph()

    def build_from_metadata(self, metadata: List[Dict[str, Any]], max_nodes: int = 60, min_degree: int = 1):
        """
        Builds a clean, optimized dependency graph from code metadata.
        Filters out low-signal isolated noise to prevent visual clumping.
        """
        raw_graph = nx.DiGraph()
        
        for item in metadata:
            file_path = item["file_path"]
            name = item["name"]
            snippet_type = item.get("type", "symbol")
            
            node_id = f"{file_path}:{name}"
            raw_graph.add_node(node_id, label=name, type=snippet_type, file=file_path)
            
            code = item.get("code_snippet", "")
            for other_item in metadata:
                other_name = other_item["name"]
                if other_name != name and f"{other_name}(" in code:
                    other_id = f"{other_item['file_path']}:{other_name}"
                    raw_graph.add_edge(node_id, other_id)

        # Filter nodes: retain nodes that have at least min_degree or are in top connected components
        degrees = dict(raw_graph.degree())
        sorted_nodes = sorted(degrees.keys(), key=lambda n: degrees[n], reverse=True)
        
        selected_nodes = set(sorted_nodes[:max_nodes]) if len(sorted_nodes) > max_nodes else set(sorted_nodes)
        if min_degree > 0:
            selected_nodes = {n for n in selected_nodes if degrees[n] >= min_degree}
        
        if not selected_nodes and raw_graph.nodes:
            selected_nodes = set(list(raw_graph.nodes)[:20])

        self.graph = raw_graph.subgraph(selected_nodes).copy()

    def get_visualization(self, layout_type: str = "spring"):
        if len(self.graph.nodes) == 0:
            fig = go.Figure()
            fig.update_layout(
                paper_bgcolor='#ffffff',
                plot_bgcolor='#ffffff',
                annotations=[dict(text="No dependencies detected for current filter criteria", showarrow=False, font=dict(color="#64748b", size=14, family="Plus Jakarta Sans"))],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                margin=dict(b=20, l=20, r=20, t=20)
            )
            return fig

        n_nodes = len(self.graph.nodes)
        
        # Layout calculation with tuned repulsion parameters
        if layout_type == "circular" or n_nodes <= 8:
            pos = nx.circular_layout(self.graph)
        elif layout_type == "kamada":
            try:
                pos = nx.kamada_kawai_layout(self.graph)
            except Exception:
                k_val = max(1.2, 3.5 / math.sqrt(n_nodes))
                pos = nx.spring_layout(self.graph, k=k_val, iterations=100, seed=42)
        else: # spring
            k_val = max(1.2, 3.5 / math.sqrt(n_nodes))
            pos = nx.spring_layout(self.graph, k=k_val, iterations=100, seed=42)

        edge_x = []
        edge_y = []
        for edge in self.graph.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])

        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=1.3, color='rgba(148, 163, 184, 0.45)'),
            hoverinfo='none',
            mode='lines'
        )

        node_x = []
        node_y = []
        node_text = []
        node_hover = []
        node_sizes = []
        node_colors = []

        degrees = dict(self.graph.degree())
        max_deg = max(degrees.values()) if degrees else 1

        for node in self.graph.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            label = self.graph.nodes[node]['label']
            node_type = self.graph.nodes[node].get('type', 'symbol')
            file_p = self.graph.nodes[node].get('file', '')
            deg = degrees[node]
            
            # Smart Labeling: Only render text overlay for high-degree hubs to eliminate clutter
            if deg >= 2 or n_nodes <= 20:
                node_text.append(label)
            else:
                node_text.append("")

            node_hover.append(
                f"<b>{label}</b><br>"
                f"📁 File: {file_p}<br>"
                f"🏷️ Type: {node_type}<br>"
                f"🔗 Degree: {deg} (In: {self.graph.in_degree(node)}, Out: {self.graph.out_degree(node)})"
            )
            node_sizes.append(max(14, min(34, 14 + (deg / max_deg) * 20)))
            node_colors.append(deg)

        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            hoverinfo='text',
            hovertext=node_hover,
            text=node_text,
            textposition="top center",
            textfont=dict(family="Plus Jakarta Sans, sans-serif", size=10, color="#1e293b"),
            marker=dict(
                showscale=True,
                colorscale=[[0, '#6366f1'], [0.5, '#06b6d4'], [1.0, '#f97316']],
                size=node_sizes,
                color=node_colors,
                line=dict(width=1.8, color='#ffffff'),
                colorbar=dict(
                    thickness=10,
                    title=dict(text="Degree", font=dict(color="#64748b", size=11, family="Plus Jakarta Sans")),
                    tickfont=dict(color="#475569", size=10, family="Plus Jakarta Sans"),
                    xanchor="left",
                    bgcolor="rgba(255, 255, 255, 0.9)",
                    bordercolor="#e2e8f0",
                    borderwidth=1
                )
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
                margin=dict(b=25, l=20, r=20, t=30),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
            )
        )
        return fig
