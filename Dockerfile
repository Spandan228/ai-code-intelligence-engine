# ==========================================
# AI Code Intelligence Engine - Dockerfile
# ==========================================

FROM python:3.10-slim

# Prevent Python from writing .pyc files & buffer output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies (build-essential, git, libgomp1 for OpenMP/FAISS)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    libgomp1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project source code
COPY . .

# Expose API (8000) and Streamlit (8501) ports
EXPOSE 8000
EXPOSE 8501

# Default command: Start both FastAPI and Streamlit using a startup script or uvicorn
CMD ["sh", "-c", "python -m uvicorn api.server:app --host 0.0.0.0 --port 8000 & python -m streamlit run ui/dashboard.py --server.port 8501 --server.address 0.0.0.0 --server.headless true"]
