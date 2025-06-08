from haystack_integrations.components.generators.ollama import OllamaGenerator

class LLM:
    @staticmethod
    def get_text_generator():
        """
        Returns a backed in generator for current LLM.
        """
        return OllamaGenerator(
            model="llama3.2",
            url="http://localhost:11434",
            generation_kwargs={"num_predict": 100, "temperature": 0.9} #play with this param should reduce galicination from LLM
        )
