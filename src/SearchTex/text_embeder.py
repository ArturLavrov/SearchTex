from haystack.components.embedders import SentenceTransformersTextEmbedder
from document_store import SingletonMeta

class TextEmbeder(metaclass=SingletonMeta):
    def __int__(self):
        self.textEmbedder = SentenceTransformersTextEmbedder(model="sentence-transformers/all-MiniLM-L6-v2")

    def warm_up(self):
        self.textEmbedder.warm_up()