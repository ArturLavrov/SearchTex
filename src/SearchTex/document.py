from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack.dataclasses import Document as HaystackDocument
class Document:
    def __init__(self, content: str):
        self.content = content
        self.embeddings = None
        #TODO: extract to document_embeder class
        self.document_embeder = SentenceTransformersDocumentEmbedder(model="sentence-transformers/all-MiniLM-L6-v2")
        self.document_embeder.warm_up()

    def generate_embeddings(self):
        doc = HaystackDocument(content=self.content)
        embedded_result = self.document_embeder.run([doc])
        self.embeddings = embedded_result["documents"][0].embedding

    def get_embeddings(self):
        return self.embeddings