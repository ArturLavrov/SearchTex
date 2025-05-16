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

---

## 🧩 API Endpoints

### `GET /query`
Query the system with a natural language question.
```http
POST /query
Content-Type: application/json

{
  "query": "How do I deploy the billing service?"
}
```
**Response:**
```json
{
  "answer": "To deploy the billing service, follow these steps...",
  "sources": [
    {
      "document": "deployment_guide.md",
      "snippet": "..."
    }
  ]
}
```

### `POST /upload`
Upload and ingest a new document.
```http
POST /upload
Content-Type: multipart/form-data

file: <your_pdf_or_markdown_file>
```
**Response:**
```json
{
  "status": "success",
  "filename": "guide.pdf"
}
```

---


## 📢 License
MIT License. Feel free to use and contribute!

---
