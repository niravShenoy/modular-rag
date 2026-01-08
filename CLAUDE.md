# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an **Agentic RAG (Retrieval-Augmented Generation)** monorepo combining a FastAPI backend with a Next.js frontend. The application enables document ingestion and AI-powered chat interactions with retrieval capabilities.

## Architecture

### Backend Architecture
- **Framework**: FastAPI with async/await throughout
- **Entry Point**: `backend/src/main.py`
- **Port**: 8000 (API docs at `/docs`)
- **Key Pattern**: Dependency injection via FastAPI `Depends()` for config and vector store access
- **Lifecycle**: Vector store is managed in FastAPI app lifespan context manager for graceful initialization and persistence
- **API Routes**: All endpoints prefixed with `/v1`:
  - `POST /v1/chat` - Send query and get RAG response
  - `POST /v1/ingest` - Upload and process documents
  - `POST /v1/config` - Update system configuration

### RAG Pipeline
```
Documents (PDF/TXT) → Ingestion → Chunking → Embeddings → ChromaDB Vector Store
                                                              ↓
User Query → Retrieval → LLM Generation → Response
```

Key modules in `backend/src/rag/`:
- **ingestion.py**: Handles document loading and chunking
- **embedding.py**: Generates embeddings (Sentence Transformers, OpenAI, HuggingFace)
- **retriever.py**: Retrieves relevant chunks and generates responses via LLM
- **vector_store.py**: ChromaDB interface (in-memory by default, persisted to disk)
- **chunking.py**: Text splitting strategies (configurable chunk size/overlap)
- **prompts.py**: System and context prompts for RAG

### Frontend Architecture
- **Framework**: Next.js 16 with App Router (Server + Client Components)
- **Port**: 3000
- **Styling**: Tailwind CSS 4 with HeroUI component library
- **State Management**: localStorage for chat history (MVP implementation, no database yet)
- **Type Safety**: Full TypeScript with strict tsconfig
- **Key Pages**:
  - `/` - Main chat interface (ChatInterface.tsx)
  - `/admin` - Document upload and management (FileUploadPanel.tsx)

## Development Commands

### Backend

```bash
# Install dependencies (from root directory)
uv sync

# Run backend server (watches for changes)
uv run backend/src/main.py

# Run single test
pytest tests/path/to/test_file.py::test_function_name -v

# Run all tests
pytest tests/ -v

# Run tests with coverage
pytest tests/ -v --cov=backend/src
```

### Frontend

```bash
# Navigate to UI directory first
cd ui

# Install dependencies
npm install

# Development server (hot reload)
npm run dev

# Production build
npm run build

# Run production server
npm start

# Linting
npm run lint
```

### Running Full Application

Open two terminal windows:
- **Terminal 1**: `uv run backend/src/main.py`
- **Terminal 2**: `cd ui && npm run dev`

Then access at `http://localhost:3000`

## Code Standards

- **Type Hints**: Required on all Python functions (use `from typing import ...`)
- **Line Length**: 100 characters max (PEP 8)
- **Python Version**: 3.10+ (specified in pyproject.toml)
- **Validation**: Pydantic BaseModel for all API request/response schemas in `backend/src/models/schemas.py`
- **Testing Framework**: pytest with fixtures in `tests/conftest.py`
- **API Documentation**: Auto-generated at `/docs` via FastAPI

## Configuration

**Configuration File**: `config/default.yaml`
- Embeddings model selection
- Vector store settings
- LLM model choice (Groq, Ollama, OpenAI)
- Chunking parameters (chunk_size, overlap)
- Retrieval settings (top_k for results)
- System prompts for RAG

Configuration is loaded via `Config` class in `backend/src/core/config.py` and injected into handlers via FastAPI dependencies.

## Important Design Patterns

### 1. Dependency Injection
All route handlers receive dependencies via `Depends()`:
```python
async def chat(request: ChatRequest, config: Config = Depends(get_config)):
    # Use config and vector store
```

### 2. Vector Store Lifecycle
The `VectorStoreService` is created once on app startup and reused across requests. It's stored in `app.state.vector_store`. This avoids reloading embeddings for every request.

### 3. Async-First Design
All I/O operations are async. Use `async def` for route handlers and async libraries (langchain async methods when available).

### 4. Pydantic Validation
All API input is validated through Pydantic schemas. Invalid input returns 422 Unprocessable Entity automatically.

## File Organization Notes

- **`backend/src/api/dependencies.py`**: Where `get_config()` and `get_vector_store()` are defined—modify here to add new dependencies
- **`backend/src/api/routers/`**: Each file is a router blueprint registered in main.py
- **`ui/src/app/`**: Next.js App Router pages (anything in subdirectories becomes a route)
- **`ui/src/components/`**: Reusable React components
- **`data/`**: Git-ignored directory for uploaded PDFs and text files

## Common Workflows

### Adding a New API Endpoint
1. Create request/response schema in `backend/src/models/schemas.py`
2. Add route handler in appropriate router file (`backend/src/api/routers/`)
3. Use `Depends(get_config)` and `Depends(get_vector_store)` for dependencies
4. Register router in `backend/src/main.py` if new file
5. Test at `http://localhost:8000/docs`

### Modifying RAG Behavior
1. Adjust prompts in `backend/src/rag/prompts.py`
2. Modify retrieval logic in `backend/src/rag/retriever.py`
3. Change embedding/LLM via `config/default.yaml`
4. No restart needed if using config endpoint—config can be updated at runtime

### Adding Frontend Features
1. Create component in `ui/src/components/` or page in `ui/src/app/`
2. Use HeroUI components for consistent styling
3. Call backend API endpoints using fetch or client-side libraries
4. TypeScript will catch most issues before runtime

## Notes on Current Implementation

- **Chat History**: Currently stored in browser localStorage only (MVP state)
- **Authentication**: Not yet implemented (routes are unauthenticated)
- **Persistence**: Vector store persists to disk in `./data` directory
- **JWT Tokens**: Not currently used, but framework is ready for implementation
