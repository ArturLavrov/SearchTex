from flask import Flask, request, jsonify
from haystack.core.pipeline import Pipeline
from haystack.dataclasses import Document
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever
from haystack.components.builders.prompt_builder import PromptBuilder
from haystack_integrations.components.generators.ollama import OllamaGenerator
from pypdf import PdfReader
from markdown_it import MarkdownIt
import io

# --- Init Flask app and Haystack components ---
app = Flask(__name__)
document_store = InMemoryDocumentStore(embedding_similarity_function="cosine")
document_embeder = SentenceTransformersDocumentEmbedder(model="sentence-transformers/all-MiniLM-L6-v2")
document_embeder.warm_up()
text_embeder = SentenceTransformersTextEmbedder(model="sentence-transformers/all-MiniLM-L6-v2")
text_embeder.warm_up()

retriever = InMemoryEmbeddingRetriever(document_store=document_store)
generator = OllamaGenerator(
    model="llama3.2",
    url="http://localhost:11434",
    generation_kwargs={"num_predict": 100, "temperature": 0.9}
)
prompt_template = """
You're a helpful assistant answering questions based only on the information provided below.
Please do not rely on your own knowledge or make assumptions beyond the context.

If the answer is not explicitly available, say: "I'm sorry, I couldn't find enough information to answer that."

---

Context:
{% for document in documents %}
{{ document.content }}
{% endfor %}

---

Question from user: {{ question }}?

Your answer:
"""
prompt_builder = PromptBuilder(template=prompt_template)

# Pipeline
pipeline = Pipeline()
pipeline.add_component("text_embedder", text_embeder)
pipeline.add_component("retriever", retriever)
pipeline.add_component("prompt_builder", prompt_builder)
pipeline.add_component("llm", generator)
pipeline.connect("text_embedder.embedding", "retriever.query_embedding")
pipeline.connect("retriever", "prompt_builder.documents")
pipeline.connect("prompt_builder", "llm")

md = MarkdownIt()

# --- Utils ---
def parse_pdf(file_bytes: bytes) -> str:
    reader = PdfReader(io.BytesIO(file_bytes))
    return "\n".join([page.extract_text() or "" for page in reader.pages])

def parse_markdown(file_bytes: bytes) -> str:
    text = file_bytes.decode("utf-8")
    tokens = md.parse(text)
    return "\n".join([t.content for t in tokens if t.type == "inline"])

# --- Routes ---
@app.route("/upload", methods=["POST"])
def upload():
    #implement document preprocessing
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    filename = file.filename
    file_bytes = file.read()

    if filename.endswith(".pdf"):
        text = parse_pdf(file_bytes)
    elif filename.endswith(".md") or filename.endswith(".markdown"):
        text = parse_markdown(file_bytes)
    else:
        return jsonify({"error": "Unsupported file type"}), 400

    doc = Document(content=text)
    embedded_result = document_embeder.run([doc])
    doc.embedding = embedded_result["documents"][0].embedding
    document_store.write_documents([doc])

    return jsonify({"message": f"{filename} uploaded and embedded."})

@app.route("/query", methods=["GET"])
def query():
    user_query = request.args.get("query", "")
    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    result = pipeline.run({"text_embedder": {"text": user_query}, "prompt_builder": {"question": user_query}})
    return jsonify({"response": result["llm"]["replies"][0]})

# --- Entry Point ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
