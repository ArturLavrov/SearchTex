from haystack_integrations.components.generators.ollama import OllamaGenerator
from config import Config


class LLM:
    @staticmethod
    def get_text_generator():
        """
        Returns a backed in generator for current LLM.
        """
        return OllamaGenerator(
            model=Config.get("LLM_MODEL_NAME"),
            url=Config.get("LLM_URL"),
            generation_kwargs={"num_predict": 100, "temperature": 0.9}
        )
