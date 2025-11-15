# Configurable RAG Pipeline

Configurable Retrieval-Augmented Generation pipeline with a pluggable API interface for multi-domain applications.

## Code Structure

```
.
├── .env                  # Environment variables
├── .gitignore            # Git ignore file
├── .python-version       # Python version
├── main.py               # Main application entry point
├── pyproject.toml        # Project configuration and dependencies
├── README.md             # This file
├── uv.lock               # uv lock file
├── config/
│   └── default.yaml      # Default configuration
├── data/                 # Data files (ignored by git)
│   ├── pdf_files/        # PDF files for ingestion
│   └── text_files/       # Text files for ingestion
├── src/
│   ├── api/              # API related files
│   │   ├── dependencies.py # API dependencies
│   │   └── routers/      # API routers
│   │       ├── chat_router.py
│   │       ├── config_router.py
│   │       └── ingestion_router.py
│   ├── core/
│   │   └── config.py     # Configuration loading
│   ├── models/
│   │   └── schemas.py    # Pydantic schemas
│   └── rag/
│       ├── embedding.py  # Embedding models
│       ├── ingestion.py  # Data ingestion logic
│       └── retriever.py  # Retriever logic
└── tests/                # Tests
```

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    ```

2.  **Set up Python environment:**
    Make sure you have Python 3.12 installed. You can use a tool like `pyenv` to manage Python versions.

    Create and activate a virtual environment. If you have `uv` installed:
    ```bash
    uv venv
    source .venv\Scripts\activate  # On Windows
    # On macOS/Linux: source .venv/bin/activate
    ```

3.  **Install dependencies:**
    With the virtual environment activated, install the dependencies using `uv`:
    ```bash
    uv sync
    ```

4.  **Set up environment variables:**
    Create a `.env` file in the root of the project and add the necessary environment variables.

    ```
    # .env
    # Add your environment variables here
    # e.g. OPENAI_API_KEY="your-key-here"
    ```
