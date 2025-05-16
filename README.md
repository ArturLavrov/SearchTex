# ![SearchTex Logo](https://github.com/user-attachments/assets/707ebc8a-fb2f-4cbd-8341-7ad060fe5ec0)

# SearchTex

**SearchTex** is an intelligent search engine that simplifies access to any type of documentation(internal company documentation, personal docs, etc...) using semantic retrieval and natural language queries. Powered by Retrieval-Augmented Generation (RAG), it delivers fast, context-aware answers without needing exact keyword matches.

---

## 🚀 Features

- 🔍 Semantic search powered by vector embeddings (e.g., FAISS)
- 🧠 LLM-backed natural language answer generation
- 📄 Support for PDF and Markdown document ingestion
---

## 🧭 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/your-org/searchtex.git
cd searchtex
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
uvicorn main:app --reload
```

---

## 📁 Directory Structure
```
searchtex/
├── app/                 # Core logic (retriever, generator, parser)
├── docs/                # Sample documentation files
├── static/              # Logo and assets
├── main.py              # FastAPI entry point
└── README.md
```

---


## 📢 License
MIT License. Feel free to use and contribute!

---
