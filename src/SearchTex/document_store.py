from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.dataclasses import Document as HaystackDocument
import threading


class SingletonMeta(type):
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class DocumentStore(metaclass=SingletonMeta):
    def __init__(self):
        self.document_store = InMemoryDocumentStore(embedding_similarity_function="cosine")

    def add_document(self, doc):
        storage_document = HaystackDocument(content=doc.get_content())
        storage_document.embedding = doc.get_embeddings()
        self.document_store.write_documents([storage_document])

    def get_instance(self):
        return self.document_store
