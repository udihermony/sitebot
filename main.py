# import tkinter as tk
# from tkinter import scrolledtext, messagebox, ttk
# from urllib.parse import urlparse, urljoin
# from sitebot.llm_interface import LlamaInterface
# from collections import defaultdict
# import networkx as nx
# import threading
# import queue
# import requests
# from bs4 import BeautifulSoup

# class WebCrawler:
#     def __init__(self, root_url, max_pages=50):
#         self.root_url = root_url
#         self.max_pages = max_pages
#         self.visited_urls = set()
#         parsed_url = urlparse(root_url)
#         self.allowed_domain = parsed_url.netloc
#         self.allowed_path = parsed_url.path

#     def crawl(self):
#         queue = [self.root_url]
#         while queue and len(self.visited_urls) < self.max_pages:
#             url = queue.pop(0)
#             if url not in self.visited_urls and self.is_valid_url(url):
#                 try:
#                     page_content = self.fetch_page(url)
#                     self.visited_urls.add(url)
#                     links = self.extract_links(url, page_content)
#                     yield {'url': url, 'text': self.extract_text(page_content), 'links': links}
#                     queue.extend(link for link in links if link not in self.visited_urls)
#                 except Exception as e:
#                     print(f"Error crawling {url}: {str(e)}")

#     def fetch_page(self, url):
#         response = requests.get(url, headers={'User-Agent': 'SiteBot Crawler'})
#         response.raise_for_status()
#         return response.text

#     def extract_links(self, base_url, content):
#         soup = BeautifulSoup(content, 'html.parser')
#         links = []
#         for a_tag in soup.find_all('a', href=True):
#             link = urljoin(base_url, a_tag['href'])
#             if self.is_valid_url(link):
#                 links.append(link)
#         return links

#     def is_valid_url(self, url):
#         parsed_url = urlparse(url)
#         return (parsed_url.netloc == self.allowed_domain and
#                 parsed_url.path.startswith(self.allowed_path))

#     def extract_text(self, content):
#         soup = BeautifulSoup(content, 'html.parser')
#         for script in soup(["script", "style"]):
#             script.decompose()
#         return soup.get_text(separator=' ', strip=True)


# class ChatWindow:
#     def __init__(self, master, sitebot):
#         self.master = master
#         self.sitebot = sitebot
        
#         master.title("SiteBot Chat")
#         master.geometry("500x600")

#         self.chat_area = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=60, height=30)
#         self.chat_area.pack(padx=10, pady=10)
#         self.chat_area.config(state=tk.DISABLED)

#         self.query_entry = tk.Entry(master, width=50)
#         self.query_entry.pack(padx=10, pady=5)

#         self.ask_button = tk.Button(master, text="Ask", command=self.ask_question)
#         self.ask_button.pack(pady=5)

#         self.status_label = tk.Label(master, text="")
#         self.status_label.pack(pady=5)

#     def ask_question(self):
#         query = self.query_entry.get()
#         if not query:
#             messagebox.showerror("Error", "Please enter a question")
#             return

#         self.status_label.config(text="Processing question...")
#         self.ask_button.config(state=tk.DISABLED)
#         threading.Thread(target=self.process_question, args=(query,), daemon=True).start()

#     def process_question(self, query):
#         response = self.sitebot.process_user_query(query)
#         self.master.after(0, self.display_answer, query, response)

#     def display_answer(self, query, response):
#         self.chat_area.config(state=tk.NORMAL)
#         self.chat_area.insert(tk.END, f"\nYou: {query}\n\nSiteBot: {response}\n\n")
#         self.chat_area.see(tk.END)
#         self.chat_area.config(state=tk.DISABLED)
#         self.status_label.config(text="")
#         self.ask_button.config(state=tk.NORMAL)
#         self.query_entry.delete(0, tk.END)

# class SiteBotGUI:
#     def __init__(self, master):
#         self.master = master
#         master.title("SiteBot Crawler")
#         master.geometry("600x500")

#         self.sitebot = None
#         self.crawl_queue = queue.Queue()

#         self.url_label = tk.Label(master, text="Enter website URL:")
#         self.url_label.pack()

#         self.url_entry = tk.Entry(master, width=50)
#         self.url_entry.pack()

#         self.pages_label = tk.Label(master, text="Maximum Pages to Crawl:")
#         self.pages_label.pack()

#         self.pages_entry = tk.Entry(master, width=5)
#         self.pages_entry.insert(0, "50")  # Default max pages
#         self.pages_entry.pack()

#         self.crawl_button = tk.Button(master, text="Crawl Website", command=self.start_crawl)
#         self.crawl_button.pack()

#         self.progress_bar = ttk.Progressbar(master, orient="horizontal", length=300, mode="determinate")
#         self.progress_bar.pack()

#         self.status_label = tk.Label(master, text="")
#         self.status_label.pack()

#         self.output_area = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=70, height=20)
#         self.output_area.pack()

#     def start_crawl(self):
#         url = self.url_entry.get()
#         if not url:
#             messagebox.showerror("Error", "Please enter a URL")
#             return

#         try:
#             max_pages = int(self.pages_entry.get())
#             if max_pages < 1:
#                 raise ValueError
#         except ValueError:
#             messagebox.showerror("Error", "Please enter a valid positive integer for maximum pages")
#             return

#         self.sitebot = SiteBot(url, max_pages, self.crawl_queue)
#         self.output_area.insert(tk.END, f"Starting crawl of {url} with max {max_pages} pages\n")
#         self.crawl_button.config(state=tk.DISABLED)
#         self.progress_bar["maximum"] = max_pages
#         self.progress_bar["value"] = 0
#         self.status_label.config(text="Crawling in progress...")
        
#         threading.Thread(target=self.crawl_thread, daemon=True).start()
#         self.master.after(100, self.check_crawl_queue)

#     def crawl_thread(self):
#         self.sitebot.crawl_and_process_website()
#         self.crawl_queue.put(("DONE", None))

#     def check_crawl_queue(self):
#         try:
#             message, data = self.crawl_queue.get_nowait()
#             if message == "UPDATE":
#                 self.output_area.insert(tk.END, f"Crawled: {data}\n")
#                 self.output_area.see(tk.END)
#                 self.progress_bar["value"] += 1
#             elif message == "DONE":
#                 self.crawl_completed()
#             self.master.after(100, self.check_crawl_queue)
#         except queue.Empty:
#             self.master.after(100, self.check_crawl_queue)

#     def crawl_completed(self):
#         self.crawl_button.config(state=tk.NORMAL)
#         self.status_label.config(text="Crawl completed")
#         self.output_area.insert(tk.END, "Crawl completed.\n")
#         overview = self.sitebot.get_site_overview()
#         self.output_area.insert(tk.END, f"Site Overview:\n{overview}\n")
#         self.output_area.see(tk.END)
        
#         # Open chat window
#         chat_window = tk.Toplevel(self.master)
#         ChatWindow(chat_window, self.sitebot)


# class SiteBotGUI:
#     def __init__(self, master):
#         self.master = master
#         master.title("SiteBot")
#         master.geometry("600x550")

#         self.sitebot = None
#         self.crawl_queue = queue.Queue()

#         self.url_label = tk.Label(master, text="Enter website URL:")
#         self.url_label.pack()

#         self.url_entry = tk.Entry(master, width=50)
#         self.url_entry.pack()

#         self.pages_label = tk.Label(master, text="Maximum Pages to Crawl:")
#         self.pages_label.pack()

#         self.pages_entry = tk.Entry(master, width=5)
#         self.pages_entry.insert(0, "50")  # Default max pages
#         self.pages_entry.pack()

#         self.crawl_button = tk.Button(master, text="Crawl Website", command=self.start_crawl)
#         self.crawl_button.pack()

#         self.progress_bar = ttk.Progressbar(master, orient="horizontal", length=300, mode="determinate")
#         self.progress_bar.pack()

#         self.status_label = tk.Label(master, text="")
#         self.status_label.pack()

#         self.query_label = tk.Label(master, text="Enter your question:")
#         self.query_label.pack()

#         self.query_entry = tk.Entry(master, width=50)
#         self.query_entry.pack()

#         self.query_button = tk.Button(master, text="Ask Question", command=self.ask_question)
#         self.query_button.pack()

#         self.output_area = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=70, height=20)
#         self.output_area.pack()

#     def start_crawl(self):
#         url = self.url_entry.get()
#         if not url:
#             messagebox.showerror("Error", "Please enter a URL")
#             return

#         try:
#             max_pages = int(self.pages_entry.get())
#             if max_pages < 1:
#                 raise ValueError
#         except ValueError:
#             messagebox.showerror("Error", "Please enter a valid positive integer for maximum pages")
#             return

#         self.sitebot = SiteBot(url, max_pages, self.crawl_queue)
#         self.output_area.insert(tk.END, f"Starting crawl of {url} with max {max_pages} pages\n")
#         self.crawl_button.config(state=tk.DISABLED)
#         self.progress_bar["maximum"] = max_pages
#         self.progress_bar["value"] = 0
#         self.status_label.config(text="Crawling in progress...")
        
#         threading.Thread(target=self.crawl_thread, daemon=True).start()
#         self.master.after(100, self.check_crawl_queue)

#     def crawl_thread(self):
#         self.sitebot.crawl_and_process_website()
#         self.crawl_queue.put(("DONE", None))

#     def check_crawl_queue(self):
#         try:
#             message, data = self.crawl_queue.get_nowait()
#             if message == "UPDATE":
#                 self.output_area.insert(tk.END, f"Crawled: {data}\n")
#                 self.output_area.see(tk.END)
#                 self.progress_bar["value"] += 1
#             elif message == "DONE":
#                 self.crawl_completed()
#             self.master.after(100, self.check_crawl_queue)
#         except queue.Empty:
#             self.master.after(100, self.check_crawl_queue)

#     def crawl_completed(self):
#         self.crawl_button.config(state=tk.NORMAL)
#         self.status_label.config(text="Crawl completed")
#         self.output_area.insert(tk.END, "Crawl completed.\n")
#         overview = self.sitebot.get_site_overview()
#         self.output_area.insert(tk.END, f"Site Overview:\n{overview}\n")
#         self.output_area.see(tk.END)

#     def ask_question(self):
#         if not self.sitebot:
#             messagebox.showerror("Error", "Please crawl a website first")
#             return

#         query = self.query_entry.get()
#         if not query:
#             messagebox.showerror("Error", "Please enter a question")
#             return

#         self.status_label.config(text="Processing question...")
#         self.query_button.config(state=tk.DISABLED)
#         threading.Thread(target=self.process_question, args=(query,), daemon=True).start()

#     def process_question(self, query):
#         response = self.sitebot.process_user_query(query)
#         self.master.after(0, self.display_answer, query, response)

#     def display_answer(self, query, response):
#         self.output_area.insert(tk.END, f"\nQ: {query}\nA: {response}\n\n")
#         self.output_area.see(tk.END)
#         self.status_label.config(text="")
#         self.query_button.config(state=tk.NORMAL)


# class SiteBot:
#     def __init__(self, root_url, max_pages, queue):
#         self.root_url = root_url
#         self.web_crawler = WebCrawler(root_url, max_pages)
#         self.llm = LlamaInterface()
#         self.knowledge_base = defaultdict(dict)
#         self.graph = nx.DiGraph()
#         self.queue = queue

#     def crawl_and_process_website(self):
#         for page_info in self.web_crawler.crawl():
#             url = page_info['url']
#             self.queue.put(("UPDATE", url))
            
#             summary = self.llm.summarize(page_info['text'], max_length=50)
#             entities = self.llm.extract_entities(page_info['text'])
#             category = self.llm.classify_content(page_info['text'])
            
#             self.knowledge_base[url] = {
#                 'summary': summary,
#                 'entities': entities,
#                 'category': category,
#                 'links': page_info['links']
#             }
            
#             self.graph.add_node(url, summary=summary, category=category)
#             for link in page_info['links']:
#                 self.graph.add_edge(url, link)

#     def find_relevant_pages(self, query, top_n=3):
#         relevance_scores = {}
#         for url, info in self.knowledge_base.items():
#             context = f"Summary: {info['summary']}\nCategory: {info['category']}\nEntities: {info['entities']}"
#             relevance_prompt = f"On a scale of 0 to 10, how relevant is the following content to the query '{query}'? Please respond with just a number."
#             relevance_response = self.llm.generate(relevance_prompt + f"\n\nContent: {context}", max_tokens=50)
            
#             # Extract the numeric score from the response
#             score_match = re.search(r'\b([0-9]|10)\b', relevance_response)
#             if score_match:
#                 relevance_score = float(score_match.group(1))
#             else:
#                 print(f"Couldn't parse relevance score for {url}. Response: {relevance_response}")
#                 relevance_score = 0  # Default to 0 if we can't parse a score
            
#             relevance_scores[url] = relevance_score
        
#         return sorted(relevance_scores.items(), key=lambda x: x[1], reverse=True)[:top_n]


#     def process_user_query(self, query):
#         relevant_pages = self.find_relevant_pages(query)
        
#         if not relevant_pages:
#             return "I'm sorry, I couldn't find any relevant information for your query."
        
#         context = "\n".join([f"Page: {url}\nSummary: {self.knowledge_base[url]['summary']}" for url, _ in relevant_pages])
        
#         answer_prompt = f"Given the following context from a website, please answer the user's query.\n\nContext:\n{context}\n\nUser Query: {query}\n\nAnswer:"
#         answer = self.llm.generate(answer_prompt, max_tokens=200)
        
#         source_urls = [url for url, _ in relevant_pages]
#         answer += f"\n\nSources: {', '.join(source_urls)}"
        
#         return answer

#     def get_site_overview(self):
#         total_pages = len(self.knowledge_base)
#         categories = set(info['category'] for info in self.knowledge_base.values())
        
#         overview_prompt = f"Create a brief overview of a website based on the following information:\n"
#         overview_prompt += f"Total pages: {total_pages}\n"
#         overview_prompt += f"Categories: {', '.join(categories)}\n"
#         overview_prompt += "Top 5 most connected pages:\n"
        
#         top_pages = sorted(self.graph.degree, key=lambda x: x[1], reverse=True)[:5]
#         for page, degree in top_pages:
#             overview_prompt += f"- {page} (connected to {degree} pages)\n"
        
#         overview = self.llm.generate(overview_prompt, max_tokens=200)
#         return overview


# def main():
#     root = tk.Tk()
#     gui = SiteBotGUI(root)
#     root.mainloop()

# if __name__ == "__main__":
#     main()



import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import threading
import queue
import requests
from bs4 import BeautifulSoup
from github import Github
import os
from sitebot.llm_interface import LlamaInterface

class RouterAgent:
    def __init__(self, repo, path="", parent=None):
        self.repo = repo
        self.path = path
        self.parent = parent
        self.llm = LlamaInterface()

    def analyze_structure(self):
        contents = self.repo.get_contents(self.path)
        folders = []
        files = []

        for content in contents:
            if content.type == "dir":
                folders.append(content.path)
            elif content.type == "file":
                files.append(content.path)

        return folders, files

    def delegate_tasks(self):
        folders, files = self.analyze_structure()
        tasks = []

        for folder in folders:
            if self.is_small_enough(folder):
                tasks.append(("summarize", folder))
            else:
                tasks.append(("route", folder))

        for file in files:
            tasks.append(("summarize", file))

        return tasks

    
    def is_small_enough(self, path):
        try:
            contents = self.repo.get_contents(path)
            return len(contents) < 5  # If folder has less than 5 items, consider it small enough
        except Exception as e:
            print(f"Error checking size of {path}: {str(e)}")
            return True  # Assume it's small enough if we can't check
        
    def process(self):
        tasks = self.delegate_tasks()
        summaries = []

        for task_type, path in tasks:
            try:
                if task_type == "summarize":
                    summarizer = SummarizerAgent(self.repo, path)
                    summaries.append(summarizer.process())
                else:
                    router = RouterAgent(self.repo, path, self)
                    summaries.extend(router.process())
            except Exception as e:
                print(f"Error processing {path}: {str(e)}")

        return self.aggregate_summaries(summaries)

    def aggregate_summaries(self, summaries):
        context = "\n".join(summaries)
        prompt = f"Aggregate the following summaries into a cohesive overview:\n\n{context}"
        return self.llm.generate(prompt, max_tokens=300)
    
    
class SummarizerAgent:
    def __init__(self, repo, path):
        self.repo = repo
        self.path = path
        self.llm = LlamaInterface()

    def process(self):
        try:
            content = self.repo.get_contents(self.path)
            if content.type == "dir":
                return self.summarize_folder()
            elif content.type == "file":
                return self.summarize_file(content)
            else:
                return f"Unknown content type for {self.path}"
        except Exception as e:
            return f"Error processing {self.path}: {str(e)}"

    def summarize_folder(self):
        try:
            contents = self.repo.get_contents(self.path)
            files = [c.path for c in contents if c.type == "file"]
            prompt = f"Summarize the purpose and content of the following folder:\n\nFolder: {self.path}\nFiles: {', '.join(files)}"
            return self.llm.generate(prompt, max_tokens=200)
        except Exception as e:
            return f"Error summarizing folder {self.path}: {str(e)}"

    def summarize_file(self, content):
        try:
            file_content = content.decoded_content.decode()
            prompt = f"Summarize the purpose and key functionality of the following file:\n\nFile: {self.path}\n\nContent:\n{file_content[:1000]}..."  # Limit content to avoid token limits
            return self.llm.generate(prompt, max_tokens=200)
        except Exception as e:
            return f"Error summarizing file {self.path}: {str(e)}"
        

class GitHubRepoAnalyzer:
    def __init__(self, repo_url):
        self.repo_url = repo_url
        self.g = Github()  # You might want to use authentication here
        self.repo = self.g.get_repo(self.extract_repo_name(repo_url))

    def extract_repo_name(self, url):
        parts = url.split('/')
        return f"{parts[-2]}/{parts[-1]}"

    def analyze(self):
        router = RouterAgent(self.repo)
        return router.process()

class AnalyzerGUI:
    def __init__(self, master):
        self.master = master
        master.title("GitHub Repository Analyzer")
        master.geometry("600x500")

        self.url_label = tk.Label(master, text="Enter GitHub Repository URL:")
        self.url_label.pack()

        self.url_entry = tk.Entry(master, width=50)
        self.url_entry.pack()

        self.analyze_button = tk.Button(master, text="Analyze Repository", command=self.start_analysis)
        self.analyze_button.pack()

        self.progress_bar = ttk.Progressbar(master, orient="horizontal", length=300, mode="indeterminate")
        self.progress_bar.pack()

        self.status_label = tk.Label(master, text="")
        self.status_label.pack()

        self.output_area = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=70, height=20)
        self.output_area.pack()

    def start_analysis(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("Error", "Please enter a GitHub repository URL")
            return

        self.analyze_button.config(state=tk.DISABLED)
        self.progress_bar.start()
        self.status_label.config(text="Analysis in progress...")

        threading.Thread(target=self.run_analysis, args=(url,), daemon=True).start()

    def run_analysis(self, url):
        try:
            analyzer = GitHubRepoAnalyzer(url)
            result = analyzer.analyze()
            self.master.after(0, self.display_result, result)
        except Exception as e:
            self.master.after(0, self.display_error, str(e))

    def display_result(self, result):
        self.output_area.insert(tk.END, f"Analysis Result:\n\n{result}\n")
        self.output_area.see(tk.END)
        self.cleanup()

    def display_error(self, error):
        messagebox.showerror("Error", f"An error occurred: {error}")
        self.cleanup()

    def cleanup(self):
        self.progress_bar.stop()
        self.analyze_button.config(state=tk.NORMAL)
        self.status_label.config(text="Analysis completed")

def main():
    root = tk.Tk()
    gui = AnalyzerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()