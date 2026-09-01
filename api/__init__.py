"""
AI Code Intelligence Engine - API Module
FastAPI REST application exposing AST parsing, FAISS search, graphs, and quality audits.
"""

from .server import app

__all__ = ["app"]
