from haystack.dataclasses import Document as HaystackDocument
from haystack_integrations.document_stores.pgvector import PgvectorDocumentStore
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
        self.document_store = PgvectorDocumentStore(
            table_name="documents",
            embedding_dimension=384, #TODO: param should be configurable and depends on embedder type
            vector_function="cosine_similarity",
            recreate_table=False,
        )

    def add_document(self, doc):
        embedding = doc.get_embeddings()
        doc_content = doc.get_content()
        storage_document = HaystackDocument(content=doc_content, embedding=embedding)
        self.document_store.write_documents([storage_document])

    def get_instance(self):
        return self.document_store
