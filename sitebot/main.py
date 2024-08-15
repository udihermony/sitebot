from sitebot.crawlers.web_crawler import WebCrawler
from sitebot.knowledge_base.graph_builder import GraphBuilder
from sitebot.agents.parsing_agent import ParsingAgent
from sitebot.agents.summarization_agent import SummarizationAgent
from sitebot.agents.classification_agent import ClassificationAgent
from sitebot.agents.entity_recognition_agent import EntityRecognitionAgent
from sitebot.user_interface.chatbot import Chatbot
from sitebot.llm_interface import LlamaInterface

class SiteBot:
    def __init__(self, root_url):
        self.root_url = root_url
        self.web_crawler = WebCrawler(root_url)
        self.graph_builder = GraphBuilder()
        self.llm = LlamaInterface()
        self.knowledge_base = {}

    def crawl_website(self):
        print("Starting website crawl...")
        for page_info in self.web_crawler.crawl():
            url = page_info['url']
            print(f"Crawled: {url}")
            
            # Use LLM to process the page content
            summary = self.llm.summarize(page_info['text'])
            entities = self.llm.extract_entities(page_info['text'])
            category = self.llm.classify_content(page_info['text'])
            
            # Store processed information in knowledge base
            self.knowledge_base[url] = {
                'summary': summary,
                'entities': entities,
                'category': category,
                'links': page_info['links']
            }
        
        print("Crawl completed.")
        self.graph_builder.build_graph(self.knowledge_base)

    def process_user_query(self, query):
        # Find the most relevant page(s) for the query
        relevant_pages = self.graph_builder.find_relevant_pages(query)
        
        if not relevant_pages:
            return "I'm sorry, I couldn't find any relevant information for your query."
        
        # Combine context from relevant pages
        context = "\n".join([self.knowledge_base[url]['summary'] for url in relevant_pages[:3]])
        
        # Use LLM to answer the query based on the context
        answer = self.llm.answer_query(query, context)
        
        return answer

def main():
    root_url = "https://example.com"  # Replace with the actual website URL
    sitebot = SiteBot(root_url)
    sitebot.crawl_website()

    while True:
        user_query = input("Enter your question (or 'quit' to exit): ")
        if user_query.lower() == 'quit':
            break
        response = sitebot.process_user_query(user_query)
        print(response)

if __name__ == "__main__":
    main()