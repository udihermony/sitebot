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
        self.llm = LlamaInterface()
        self.analysis_result = None

    def extract_repo_name(self, url):
        parts = url.split('/')
        return f"{parts[-2]}/{parts[-1]}"

    def analyze(self):
        router = RouterAgent(self.repo)
        self.analysis_result = router.process()
        return self.analysis_result

    def answer_question(self, question):
        if not self.analysis_result:
            raise Exception("Repository has not been analyzed yet")

        prompt = f"""Based on the following analysis of a GitHub repository, please answer this question: {question}

Analysis:
{self.analysis_result}

Please provide a concise and informative answer based solely on the information provided in the analysis."""

        return self.llm.generate(prompt, max_tokens=300)
    
class AnalyzerGUI:
    def __init__(self, master):
        self.master = master
        master.title("GitHub Repository Analyzer")
        master.geometry("600x600")  # Increased height to accommodate new elements

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

        # New elements for asking questions
        self.question_label = tk.Label(master, text="Ask a question about the repository:")
        self.question_label.pack()

        self.question_entry = tk.Entry(master, width=50)
        self.question_entry.pack()

        self.ask_button = tk.Button(master, text="Ask Question", command=self.ask_question)
        self.ask_button.pack()

        self.analyzer = None  # Will hold the GitHubRepoAnalyzer instance

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
            self.analyzer = GitHubRepoAnalyzer(url)
            result = self.analyzer.analyze()
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

    def ask_question(self):
        if not self.analyzer:
            messagebox.showerror("Error", "Please analyze a repository first")
            return

        question = self.question_entry.get()
        if not question:
            messagebox.showerror("Error", "Please enter a question")
            return

        self.ask_button.config(state=tk.DISABLED)
        self.status_label.config(text="Processing question...")

        threading.Thread(target=self.process_question, args=(question,), daemon=True).start()

    def process_question(self, question):
        try:
            answer = self.analyzer.answer_question(question)
            self.master.after(0, self.display_answer, answer)
        except Exception as e:
            self.master.after(0, self.display_error, str(e))

    def display_answer(self, answer):
        self.output_area.insert(tk.END, f"\nQ: {self.question_entry.get()}\nA: {answer}\n")
        self.output_area.see(tk.END)
        self.ask_button.config(state=tk.NORMAL)
        self.status_label.config(text="Question answered")
        self.question_entry.delete(0, tk.END)

def main():
    root = tk.Tk()
    gui = AnalyzerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()