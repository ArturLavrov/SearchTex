class LLMPrompt:
    def __init__(self):
        self.prompt_template = """
        You're a helpful assistant answering questions based only on the information provided below.
        Please do not rely on your own knowledge or make assumptions beyond the context.
        
        If the answer is not explicitly available, say: "I'm sorry, I couldn't find enough information to answer that."
        
        ---
        
        Context:
        {% for document in documents %}
        {{ document.content }}
        {% endfor %}
        
        ---
        
        Question from user: {{ question }}?
        
        Your answer:
        """
    def get_prompt_template(self):
        return self.prompt_template