import ollama

class LlamaInterface:
    def __init__(self, model_name="llama3.1"):
        self.model_name = model_name

    def generate(self, prompt, max_tokens=100):
        response = ollama.generate(model=self.model_name, prompt=prompt)
        return response['response']

    def summarize(self, text, max_length=100):
        prompt = f"Summarize the following text in about {max_length} words:\n\n{text}"
        return self.generate(prompt)

    def extract_entities(self, text):
        prompt = f"Extract and list the main entities (people, places, organizations, etc.) from the following text:\n\n{text}"
        return self.generate(prompt)

    def classify_content(self, text):
        prompt = f"Classify the main topic or category of the following text:\n\n{text}"
        return self.generate(prompt)

    def answer_query(self, query, context):
        prompt = f"Given the following context, answer the query:\n\nContext: {context}\n\nQuery: {query}"
        return self.generate(prompt)