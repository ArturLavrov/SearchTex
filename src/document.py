from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack.components.preprocessors import DocumentSplitter
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

    def get_content(self):
        return self.content

    def split(self):
        splitter = DocumentSplitter(split_by="sentence", split_length=4, split_threshold=3)
        splitter.warm_up()
        splitter_output = splitter.run(documents=[HaystackDocument(content=self.content)])
        split_docs = splitter_output["documents"]
        return [Document(content=doc.content) for doc in split_docs]