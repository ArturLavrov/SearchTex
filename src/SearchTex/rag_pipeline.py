from llm import LLM
from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack.components.builders.prompt_builder import PromptBuilder
from haystack.core.pipeline import Pipeline
from promt_template import LLMPrompt


class RAGPipeline:
    def __init__(self):
        self.bild_pipeline()

    def bild_pipeline(self):
        pipeline = Pipeline()
        pipeline.add_component("text_embedder", self.get_text_embeder())
        pipeline.add_component("retriever", InMemoryEmbeddingRetriever())
        pipeline.add_component("prompt_builder", PromptBuilder(template=LLMPrompt().get_prompt_template()))
        pipeline.add_component("llm", LLM().get_text_generator())
        pipeline.connect("text_embedder.embedding", "retriever.query_embedding")
        pipeline.connect("retriever", "prompt_builder.documents")
        pipeline.connect("prompt_builder", "llm")

    def run(self, user_query):
        pass

    def get_text_embeder(self):
        text_embeder = SentenceTransformersTextEmbedder(model="sentence-transformers/all-MiniLM-L6-v2")
        text_embeder.warm_up()
        return text_embeder

    def get_document_embeder(self):
        pass