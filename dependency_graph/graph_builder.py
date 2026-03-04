import networkx as nx
import plotly.graph_objects as go
from typing import List, Dict, Any
import os

class GraphBuilder:
    def __init__(self):
        self.graph = nx.DiGraph()

    def build_from_metadata(self, metadata: List[Dict[str, Any]]):
        for item in metadata:
            file_path = item["file_path"]
            name = item["name"]
            snippet_type = item["type"]
            
            node_id = f"{file_path}:{name}"
            self.graph.add_node(node_id, label=name, type=snippet_type, file=file_path)
            
            # Simple heuristic for dependencies: look for other function names in the snippet
            # In a real production system, this would use a proper call graph extracted by the parser
            code = item["code_snippet"]
            for other_item in metadata:
                other_name = other_item["name"]
                if other_name != name and f"{other_name}(" in code:
                    other_id = f"{other_item['file_path']}:{other_name}"
                    self.graph.add_edge(node_id, other_id)

    def get_visualization(self):
        pos = nx.spring_layout(self.graph, k=0.8, iterations=50)
        
        edge_x = []
        edge_y = []
        for edge in self.graph.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])

        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines')

        node_x = []
        node_y = []
        node_text = []
        for node in self.graph.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_text.append(self.graph.nodes[node]['label'])

        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            hoverinfo='text',
            text=[self.graph.nodes[node]['label'] for node in self.graph.nodes()],
            marker=dict(
                showscale=True,
                colorscale='YlGnBu',
                size=[5 + self.graph.degree(node)*2 for node in self.graph.nodes()],
                color=[self.graph.degree(node) for node in self.graph.nodes()],
                colorbar=dict(
                    thickness=15,
                    title=dict(text="Node Connections"),
                    xanchor="left"
                )
            )
        )

        fig = go.Figure(data=[edge_trace, node_trace],
                     layout=go.Layout(
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20,l=5,r=5,t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )
        return fig
