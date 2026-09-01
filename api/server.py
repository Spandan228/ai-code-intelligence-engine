from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import os
import plotly.io as pio
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import threading

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
from navigation.code_navigation import CodeNavigation
from utils.logger import logger

from fastapi.middleware.cors import CORSMiddleware

# Global core instances
embedding_gen = EmbeddingGenerator()
vector_store = FaissIndex()
search_engine = SemanticSearch(embedding_gen, vector_store)
github_indexer = GitHubIndexer(embedding_gen, vector_store)
smell_detector = CodeSmellDetector()
code_explainer = CodeExplainer(search_engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("AI Code Intelligence Engine API initializing...")
    try:
        vector_store.load()
    except Exception as e:
        logger.warning(f"Initial vector store loading skipped: {e}")
    yield
    logger.info("AI Code Intelligence Engine API stopping...")

app = FastAPI(
    title="AI Code Intelligence Engine API",
    description="Industrial Multi-Language AST Parsing, Semantic Vector Search, Topology Analytics, and Code Quality Engine.",
    version="2.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class IndexRequest(BaseModel):
    path: str

class GithubIndexRequest(BaseModel):
    url: str

class SearchRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5

class ExplainRequest(BaseModel):
    code_snippet: str

@app.get("/")
def root():
    return {
        "status": "online",
        "service": "AI Code Intelligence Engine API",
        "version": "2.0.0",
        "documentation": "/docs",
        "health_check": "/stats"
    }

@app.post("/index/local")
def index_local(request: IndexRequest):
    clean_path = request.path.strip()
    if not clean_path:
        raise HTTPException(status_code=400, detail="Repository path cannot be empty")
    
    if not os.path.exists(clean_path):
        raise HTTPException(status_code=400, detail=f"Path does not exist: '{clean_path}'")
    
    if not os.path.isdir(clean_path):
        raise HTTPException(status_code=400, detail=f"Target path is not a directory: '{clean_path}'")
    
    try:
        scanner = RepoScanner(clean_path)
        files = scanner.scan()
        orchestrator = CodeParserOrchestrator()
        
        all_metadata = []
        all_snippets = []
        for f in files:
            meta_list = orchestrator.parse_file(f)
            for meta in meta_list:
                meta["file_path"] = os.path.relpath(meta["file_path"], clean_path).replace("\\", "/")
                all_metadata.append(meta)
                all_snippets.append(meta["code_snippet"])
                
        if all_snippets:
            embeddings = embedding_gen.generate(all_snippets)
            vector_store.add_embeddings(embeddings, all_metadata)
            vector_store.save()
            return {"status": "success", "indexed_files": len(files), "snippets": len(all_snippets)}
        
        return {"status": "no_code_found", "indexed_files": len(files), "snippets": 0}
    except Exception as e:
        logger.error(f"Local indexing error for {clean_path}: {e}")
        raise HTTPException(status_code=500, detail=f"Indexing failed: {str(e)}")

@app.post("/index/github")
def index_github(request: GithubIndexRequest):
    clean_url = request.url.strip()
    if not clean_url:
        raise HTTPException(status_code=400, detail="GitHub repository URL cannot be empty")
    
    try:
        result = github_indexer.index_repo(clean_url)
        return {
            "status": "success",
            "repo_url": clean_url,
            "indexed_files": result.get("indexed_files", 0),
            "snippets": result.get("snippets", 0)
        }
    except Exception as e:
        logger.error(f"GitHub indexing error for {clean_url}: {e}")
        raise HTTPException(status_code=400, detail=f"Remote indexing failed: {str(e)}")

@app.post("/search")
def search(request: SearchRequest):
    clean_query = request.query.strip()
    if not clean_query:
        return {"results": []}
    
    limit = max(1, min(request.top_k or 5, 50))
    results = search_engine.search(clean_query, top_k=limit)
    return {"results": results}

@app.get("/stats")
def get_stats():
    return {
        "total_snippets": len(vector_store.metadata),
        "dimension": vector_store.dimension
    }

@app.get("/dependency-graph")
def get_dependency_graph():
    builder = GraphBuilder()
    builder.build_from_metadata(vector_store.metadata)
    return {"nodes": len(builder.graph.nodes), "edges": len(builder.graph.edges)}

@app.get("/architecture")
def get_architecture():
    if not vector_store.metadata:
        raise HTTPException(status_code=400, detail="Index is empty")

    fig = build_architecture_graph(vector_store.metadata)
    if not fig:
        return JSONResponse(status_code=400, content={"error": "Could not build architecture graph"})

    fig_json = pio.from_json(fig.to_json()).to_plotly_json()
    return JSONResponse(content=fig_json)

@app.get("/metrics")
def get_metrics():
    metrics = analyze_repository(vector_store.metadata)
    return metrics

@app.get("/focused-graph")
def get_focused_graph(function: str):
    clean_fn = function.strip()
    if not clean_fn:
        raise HTTPException(status_code=400, detail="Function parameter cannot be empty")
    
    if not vector_store.metadata:
        raise HTTPException(status_code=400, detail="Index is empty")
    
    fig = build_focused_graph(clean_fn, vector_store.metadata)
    if not fig:
        raise HTTPException(status_code=404, detail=f"Symbol '{clean_fn}' not found in indexed repository")
    return fig.to_dict()

@app.post("/index/clear")
def clear_index():
    vector_store.reset()
    return {"status": "success", "message": "Vector store and metadata reset successfully"}

@app.get("/refactoring/smells")
def get_code_smells():
    smells = smell_detector.analyze_repository(vector_store.metadata)
    return {"smells": smells, "count": len(smells)}

@app.get("/navigation/definition")
def get_definition(name: str):
    clean_name = name.strip()
    if not clean_name:
        return {"name": name, "definitions": []}
    
    nav = CodeNavigation(vector_store.metadata)
    definitions = nav.jump_to_definition(clean_name)
    return {"name": clean_name, "definitions": definitions}

@app.get("/navigation/usages")
def get_usages(name: str):
    clean_name = name.strip()
    if not clean_name:
        return {"name": name, "usages": []}
    
    nav = CodeNavigation(vector_store.metadata)
    usages = nav.find_usages(clean_name)
    return {"name": clean_name, "usages": usages}

@app.post("/explain")
def explain(request: ExplainRequest):
    clean_snip = request.code_snippet.strip()
    if not clean_snip:
        raise HTTPException(status_code=400, detail="Code snippet cannot be empty")
    
    explanation = code_explainer.explain_code(clean_snip)
    return {"explanation": explanation}

@app.get("/dependency-graph/full")
def get_full_dependency_graph():
    builder = GraphBuilder()
    builder.build_from_metadata(vector_store.metadata)
    fig = builder.get_visualization()
    return fig.to_dict()
