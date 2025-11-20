# Agentic RAG

A powerful and configurable Retrieval-Augmented Generation (RAG) application designed for multi-domain use cases. This project combines a robust Python backend with a modern Next.js frontend to provide a seamless experience for document ingestion and intelligent chat interactions.

## Features

- **Agentic Capabilities**: Leverages advanced RAG techniques to provide accurate and context-aware responses.
- **Modern UI**: A clean and responsive user interface built with Next.js and HeroUI for chatting and managing documents.
- **Pluggable Architecture**: Modular backend design allowing for easy customization of embeddings, retrievers, and LLMs.
- **Document Management**: Easy upload and ingestion of PDF and text files.

## Code Structure

```
.
├── .env                  # Environment variables
├── .gitignore            # Git ignore file
├── .python-version       # Python version
├── pyproject.toml        # Project configuration and dependencies
├── README.md             # This file
├── uv.lock               # uv lock file
├── backend/
│   ├── main.py           # FastAPI application entry point
│   └── src/
│       ├── api/          # API related files
│       │   ├── dependencies.py  # API dependencies
│       │   └── routers/         # API routers
│       │       ├── chat_router.py
│       │       ├── config_router.py
│       │       └── ingestion_router.py
│       ├── core/
│       │   └── config.py        # Configuration loading
│       ├── models/
│       │   └── schemas.py       # Pydantic schemas
│       └── rag/
│           ├── chunking.py      # Text chunking strategies
│           ├── embedding.py     # Embedding models
│           ├── ingestion.py     # Data ingestion logic
│           ├── prompts.py       # RAG prompts
│           ├── retriever.py     # Retriever logic
│           └── vector_store.py  # Vector store interface
├── config/
│   └── default.yaml      # Default configuration
├── data/                 # Data files (ignored by git)
│   ├── pdf_files/        # PDF files for ingestion
│   └── text_files/       # Text files for ingestion
├── tests/                # Tests
└── ui/                   # Next.js frontend
    ├── src/
    │   ├── app/          # Next.js app router
    │   │   ├── admin/    # Admin page for file uploads
    │   │   ├── layout.tsx
    │   │   ├── page.tsx  # Main chat page
    │   │   └── globals.css
    │   └── components/   # React components
    │       ├── ChatInterface.tsx
    │       ├── ChatTester.tsx
    │       ├── FileUploadPanel.tsx
    │       └── Providers.tsx
    ├── public/           # Static assets
    ├── package.json
    ├── tailwind.config.ts
    ├── tsconfig.json
    └── next.config.ts
```

## Installation

### Backend Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd agentic-rag
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

    ```env
    # .env
    # Add your environment variables here
    OPENAI_API_KEY="your-key-here"
    ```

5.  **Run the backend server:**
    ```bash
    python backend/main.py
    ```
    
    The API will be available at `http://localhost:8000`. You can view the API documentation at `http://localhost:8000/docs`.

### UI Setup

1.  **Navigate to the UI directory:**
    ```bash
    cd ui
    ```

2.  **Install Node.js dependencies:**
    Make sure you have Node.js installed (version 18 or higher recommended).
    
    ```bash
    npm install
    ```

3.  **Run the development server:**
    ```bash
    npm run dev
    ```
    
    The UI will be available at `http://localhost:3000`.

4.  **Build for production (optional):**
    ```bash
    npm run build
    npm start
    ```

### Running Both Services

For the full application, you need to run both the backend and the UI:

1. **Terminal 1** - Run the backend:
   ```bash
   python backend/main.py
   ```

2. **Terminal 2** - Run the UI:
   ```bash
   cd ui
   npm run dev
   ```

Then open your browser to `http://localhost:3000` to use the application.
