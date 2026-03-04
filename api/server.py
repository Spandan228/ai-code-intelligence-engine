from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import os

from indexer.repo_scanner import RepoScanner
from indexer.code_parser import CodeParserOrchestrator
from indexer.embedding_generator import EmbeddingGenerator
from indexer.github_indexer import GitHubIndexer
from vector_store.faiss_index import FaissIndex
from search.semantic_search import SemanticSearch
from dependency_graph.graph_builder import GraphBuilder
from refactoring.code_smell_detector import CodeSmellDetector
from analysis.repo_metrics import analyze_repository
from analysis.architecture_graph import build_architecture_graph
from analysis.focused_graph import build_focused_graph
from ai_explainer.code_explainer import CodeExplainer

app = FastAPI(title="AI Code Intelligence Engine API")

# Global instances (initialized on demand or at startup)
embedding_gen = EmbeddingGenerator()
vector_store = FaissIndex()
search_engine = SemanticSearch(embedding_gen, vector_store)
github_indexer = GitHubIndexer(embedding_gen, vector_store)
smell_detector = CodeSmellDetector()
code_explainer = CodeExplainer(search_engine)

class IndexRequest(BaseModel):
    path: str

class GithubIndexRequest(BaseModel):
    url: str

class SearchRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5

@app.post("/index/local")
async def index_local(request: IndexRequest):
    if not os.path.exists(request.path):
        raise HTTPException(status_code=400, detail="Path does not exist")
    
    scanner = RepoScanner(request.path)
    files = scanner.scan()
    orchestrator = CodeParserOrchestrator()
    
    all_metadata = []
    all_snippets = []
    for f in files:
        meta_list = orchestrator.parse_file(f)
        for meta in meta_list:
            all_metadata.append(meta)
            all_snippets.append(meta["code_snippet"])
            
    if all_snippets:
        embeddings = embedding_gen.generate(all_snippets)
        vector_store.add_embeddings(embeddings, all_metadata)
        vector_store.save()
        return {"status": "success", "indexed_files": len(files), "snippets": len(all_snippets)}
    
    return {"status": "no_code_found"}

@app.post("/index/github")
async def index_github(request: GithubIndexRequest):
    github_indexer.index_repo(request.url)
    return {"status": "success", "repo_url": request.url}

@app.post("/search")
async def search(request: SearchRequest):
    results = search_engine.search(request.query, request.top_k)
    return {"results": results}

@app.get("/stats")
async def get_stats():
    return {
        "total_snippets": len(vector_store.metadata),
        "dimension": vector_store.dimension
    }

@app.get("/dependency-graph")
async def get_dependency_graph():
    builder = GraphBuilder()
    builder.build_from_metadata(vector_store.metadata)
    return {"nodes": len(builder.graph.nodes), "edges": len(builder.graph.edges)}

import plotly.io as pio
from fastapi.responses import JSONResponse

@app.get("/architecture")
async def get_architecture():
    if not vector_store.metadata:
        raise HTTPException(status_code=400, detail="Index is empty")

    fig = build_architecture_graph(vector_store.metadata)

    if not fig:
        return {"error": "Could not build graph"}

    # Convert Plotly figure into proper JSON object
    fig_json = pio.from_json(fig.to_json()).to_plotly_json()

    return JSONResponse(content=fig_json)

@app.get("/metrics")
async def get_metrics():
    metrics = analyze_repository(vector_store.metadata)
    return metrics

@app.get("/focused-graph")
async def get_focused_graph(function: str):
    fig = build_focused_graph(function, vector_store.metadata)
    if not fig:
        raise HTTPException(status_code=404, detail="Entity not found")
    return fig.to_dict()

class ExplainRequest(BaseModel):
    code_snippet: str

@app.post("/explain")
async def explain(request: ExplainRequest):
    explanation = code_explainer.explain_code(request.code_snippet)
    return {"explanation": explanation}
