from haystack.core.pipeline import Pipeline
from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever
from haystack.components.builders.prompt_builder import PromptBuilder
from promt_template import LLMPrompt
from llm import LLM
from document_store import DocumentStore


class RagPipeline:
    def __init__(self):
        self.pipeline = Pipeline()
        self.pipeline.add_component("text_embedder", self.__get_text_embedder())
        self.pipeline.add_component("retriever", self.__get_retriever())
        self.pipeline.add_component("prompt_builder", self.__get_prompt_builder())
        self.pipeline.add_component("llm", self.__get_llm())
        self.pipeline.connect("text_embedder.embedding", "retriever.query_embedding")
        self.pipeline.connect("retriever", "prompt_builder.documents")
        self.pipeline.connect("prompt_builder", "llm")

    def run(self, user_query):
        result =  self.pipeline.run(
            {
                "text_embedder": {"text": user_query},
                "prompt_builder": {"question": user_query}
             }
        )

        return result["llm"]["replies"][0]

    @staticmethod
    def __get_text_embedder():
        #TODO: move to class user_query_embeder
        text_embeder = SentenceTransformersTextEmbedder(model="sentence-transformers/all-MiniLM-L6-v2")
        text_embeder.warm_up()
        return text_embeder

    @staticmethod
    def __get_retriever():
        haystack_document_store = DocumentStore().get_instance()
        return  InMemoryEmbeddingRetriever(document_store=haystack_document_store)

    @staticmethod
    def __get_prompt_builder():
        prompt = LLMPrompt()
        return PromptBuilder(template=prompt.get_prompt_template())

    @staticmethod
    def __get_llm():
        llm = LLM()
        return llm.get_text_generator()