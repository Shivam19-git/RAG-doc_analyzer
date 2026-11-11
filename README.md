# RAG-Doc Analyzer

A full-stack Retrieval-Augmented Generation (RAG) web application built to analyze, query, and chat with technical PDF documents using high-speed vector search and LLMs.

---

## Overview

The RAG-Doc Analyzer bridges the gap between static PDF documentation (manuals, bills of materials, schematics) and actionable intelligence. Instead of manually searching through multi-page documents, users can upload files, create semantic vector indexes, and query the documentation with fast response times.

### Key Features
- **Fast Document Ingestion:** Extracts and chunks unstructured PDF text via PyPDFLoader and RecursiveCharacterTextSplitter.
- **Vector Search and Similarity:** Embeds text chunks and persists them in a local FAISS vector store for accurate semantic retrieval.
- **Context-Grounded Generation:** Injects retrieved context directly into the model prompt to prevent hallucinations while retaining general reasoning capabilities.
- **Low-Latency Inference:** Powered by Groq's high-speed inference engine using open models.
- **Dark-Themed UI:** Clean, responsive React interface styled after modern AI chat interfaces, complete with Markdown rendering and PDF attachment flows.

---

## Tech Stack

| Layer | Technologies |
| :--- | :--- |
| **Frontend** | React, Vite, Lucide Icons, React-Markdown, CSS Modules |
| **Backend** | Python 3.11+, FastAPI, Uvicorn, Pydantic |
| **RAG & AI** | LangChain Core/Community, FAISS (Facebook AI Similarity Search), Groq Cloud API |
| **Data Processing** | PyPDF, Python-Multipart |

---

## Architecture
