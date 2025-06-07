from flask import Flask, request, jsonify
from haystack.dataclasses import Document
from file import File
from document_store import DocumentStore
from document import Document
from rag_pipeline import RagPipeline

app = Flask(__name__)

pipeline = None

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    file = File(file.filename, file.read())
    parse_result = file.parse()
    if "error" in parse_result:
        return jsonify(parse_result)

    document = Document(parse_result["text"])
    document.generate_embeddings()

    document_store = DocumentStore()
    document_store.add_document(document)

    return jsonify({"message": f"{file.file_name} uploaded and embedded."})

@app.route("/query", methods=["GET"])
def query():
    user_query = request.args.get("query", "")
    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    result = pipeline.run(user_query)
    return jsonify({"response": result})

# --- Entry Point ---
if __name__ == "__main__":
    pipeline = RagPipeline(is_pipeline_tracing_enabled=True)
    app.run(host="0.0.0.0", port=8000)

