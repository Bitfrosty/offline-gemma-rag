# Offline RAG AI Assistant

A fully offline Retrieval-Augmented Generation (RAG) AI assistant built using Gemma 4, Ollama, FastAPI, MongoDB, and llama.cpp.

This project provides a privacy-focused local AI environment capable of semantic document retrieval, contextual chat memory, and GPU-accelerated inference without relying on cloud APIs.

---

# Features

* Fully offline local LLM deployment
* Retrieval-Augmented Generation (RAG)
* Semantic vector search with embeddings
* ChatGPT-style web interface
* File upload and document ingestion
* MongoDB vector storage
* GPU acceleration with CUDA
* Multi-session chat support
* REST API backend with FastAPI
* Markdown-rendered AI responses

---

# Tech Stack

## Backend

* Python
* FastAPI
* MongoDB
* Ollama
* llama.cpp

## Frontend

* HTML
* CSS
* JavaScript

## AI / ML

* Gemma 4
* nomic-embed-text
* Vector embeddings
* Semantic search
* Retrieval-Augmented Generation (RAG)

---

# Project Architecture

```text
Frontend (HTML/CSS/JS)
        │
        ▼
FastAPI Backend
        │
        ├── Ollama / llama.cpp
        │       └── Gemma 4 Inference
        │
        ├── Embedding Pipeline
        │       └── nomic-embed-text
        │
        └── MongoDB Vector Storage
                └── Retrieved Context
```

---

# Installation

## 1. Clone Repository

```bash
git clone <your-repo-url>
cd <your-project-folder>
```

---

## 2. Install Dependencies

### Ubuntu / WSL

```bash
sudo apt update
sudo apt install python3 python3-pip mongodb -y
```

### Python Packages

```bash
pip install -r requirements.txt
```

---

## 3. Install Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Pull the required models:

```bash
ollama pull gemma4:e2b
ollama pull nomic-embed-text
```

---

## 4. Start MongoDB

```bash
mongod
```

---

## 5. Start Ollama

```bash
ollama run gemma4:e2b
```

---

## 6. Run Backend Server

```bash
python server.py
```

---

## 7. Open Frontend

Open:

```text
http://127.0.0.1:3000
```

---

# RAG Pipeline

1. Upload documents
2. Split documents into chunks
3. Generate embeddings
4. Store vectors in MongoDB
5. Retrieve relevant context
6. Inject context into model prompt
7. Generate response

---

# Why Offline AI?

This project was designed to provide:

* Full data privacy
* No cloud dependency
* Lower operational cost
* Local document processing
* Customizable AI infrastructure
