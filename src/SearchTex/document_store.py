from haystack.document_stores.in_memory import InMemoryDocumentStore

class DocumentStore:
    def __init__(self):
        self.document_store = InMemoryDocumentStore(embedding_similarity_function="cosine")

    def add_document(self, doc):
        self.document_store.write_documents([doc])