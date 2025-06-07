from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.dataclasses import Document as HaystackDocument

class DocumentStore:
    def __init__(self):
        self.document_store = InMemoryDocumentStore(embedding_similarity_function="cosine")

    def add_document(self, doc):
        storage_document = HaystackDocument()
        storage_document.embedding = doc.get_embeddings()
        self.document_store.write_documents([storage_document])