import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sitebot.llm_interface import LlamaInterface

def test_llama_interface():
    llm = LlamaInterface()
    
    # Test text generation
    print("Testing text generation:")
    prompt = "What is a qubit?"
    response = llm.generate(prompt)
    print(f"Generated text: {response}\n")

    # Test summarization
    print("Testing summarization:")
    text_to_summarize = """
    Artificial intelligence (AI) is intelligence demonstrated by machines, as opposed to natural intelligence displayed by animals including humans. 
    Leading AI textbooks define the field as the study of "intelligent agents": any system that perceives its environment and takes actions that maximize its chance of achieving its goals.
    Some popular accounts use the term "artificial intelligence" to describe machines that mimic "cognitive" functions that humans associate with the human mind, such as "learning" and "problem solving", however this definition is rejected by major AI researchers.
    """
    summary = llm.summarize(text_to_summarize, max_length=30)
    print(f"Summary: {summary}\n")

    # Test entity extraction
    print("Testing entity extraction:")
    text_for_entities = "Apple Inc. is planning to open a new office in New York City, according to CEO Tim Cook."
    entities = llm.extract_entities(text_for_entities)
    print(f"Extracted entities: {entities}\n")

    # Test content classification
    print("Testing content classification:")
    text_to_classify = "The Pythagorean theorem states that the square of the hypotenuse is equal to the sum of the squares of the other two sides."
    classification = llm.classify_content(text_to_classify)
    print(f"Classification: {classification}\n")

    # Test query answering
    print("Testing query answering:")
    context = "The capital of France is Paris. It is known for the Eiffel Tower and the Louvre museum."
    query = "What is the capital of France and what is it known for?"
    answer = llm.answer_query(query, context)
    print(f"Answer: {answer}\n")

if __name__ == "__main__":
    test_llama_interface()