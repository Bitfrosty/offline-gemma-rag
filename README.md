# Offline RAG AI Assistant

A fully offline Retrieval-Augmented Generation AI assistant built with Ollama, Gemma 4, FastAPI, MongoDB, and a local web interface.

This project allows users to chat with a local AI model, upload documents, store embedded context, and retrieve relevant information without relying on cloud APIs.

---

## Overview

This project is designed to run completely locally. It combines a local language model with document retrieval so the assistant can answer questions using uploaded files and stored context.

The system uses:

* **Ollama / Gemma 4** for local AI responses
* **nomic-embed-text** for generating document embeddings
* **MongoDB** for storing embedded document chunks
* **FastAPI** for the backend server
* **HTML, CSS, and JavaScript** for the frontend interface
* **Shell scripts** to simplify setup, startup, and shutdown

---

## Features

* Offline AI chat interface
* Retrieval-Augmented Generation
* Local document ingestion
* Semantic search using embeddings
* MongoDB-based memory storage
* FastAPI backend
* ChatGPT-style frontend
* Local setup and startup scripts
* No cloud API required

---

## Project Structure

```text
project-folder/
├── setup.sh        # Installs required dependencies
├── startall.sh     # Starts all the processes required for the model
├── shutdownall.sh  # Shuts down all the processes the model is running
├── server.sh       # Starts the local AI model server
├── backend.sh      # Starts the FastAPI backend
├── mongodb.sh      # Starts MongoDB
├── server.py       # Backend application
├── static          # Folder storing frontend pages
     └── index.html      # Main chat interface
     └── login.html      # Login page
     └── signup.html     # User signup page
├── rag.py          # Embedding and retrieval logic
├── rag_docs        # Folder storing files uploaded for rag
├── ingest.py       # File ingestion logic
└── README.md
```

---

## Required Scripts

This project uses shell scripts to manage installation and startup.

### 1. Setup

Run this once after cloning the repository:

```bash
./setup.sh
```

The `setup.sh` script installs the required system packages, Python dependencies, Ollama models, and other project requirements.

---

### 2. Start MongoDB

```bash
./mongodb.sh
```

This starts the local MongoDB database used for storing embedded document chunks and chat-related data.

---

### 3. Start the AI Model Server

```bash
./server.sh
```

This starts the local AI model server using Ollama or llama.cpp, depending on how the project is configured.

---

### 4. Start the Backend

```bash
./backend.sh
```

This starts the FastAPI backend that connects the frontend, model server, embeddings, and MongoDB database.

---

## Recommended Startup Order

Run the scripts in this order:

```bash
./mongodb.sh
./server.sh
./backend.sh
```

Or run a single script:

```bash
./startall.sh
```

After all three services are running, open the frontend in your browser.

```text
http://127.0.0.1:3000
```

---

## Stopping the Project

Stop each running service from its terminal window using:

```bash
./shutdownall.sh
```

---

## How It Works

1. The user uploads or adds documents.
2. Documents are split into smaller text chunks.
3. Each chunk is converted into an embedding.
4. Embeddings and text chunks are stored in MongoDB.
5. When the user asks a question, the backend searches for relevant chunks.
6. Retrieved context is added to the AI prompt.
7. The local model generates a response using the retrieved context.

---

## RAG Pipeline

```text
User Question
     ↓
FastAPI Backend
     ↓
Embedding Search
     ↓
MongoDB Context Retrieval
     ↓
Prompt Construction
     ↓
Local Gemma 4 Model
     ↓
AI Response
```

---

## Why This Project Is Offline

This project is built to run without cloud AI APIs. That means uploaded documents, prompts, embeddings, and generated responses remain on the local machine.

Benefits include:

* Better privacy
* No API costs
* Local control over models and data
* Ability to run without internet after setup
* Customizable AI infrastructure
