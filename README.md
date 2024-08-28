# GitHub Repository Analyzer

## Overview

The GitHub Repository Analyzer is a Python-based tool that provides an in-depth analysis of GitHub repositories using AI-powered agents. It offers a user-friendly GUI for inputting repository URLs, viewing analysis results, and asking questions about the analyzed repositories.

## Features

- Analyze GitHub repositories by breaking them down into manageable sections
- Provide summaries of repository structure and content
- Allow users to ask questions about the analyzed repositories
- User-friendly GUI interface

## Main Components

1. **RouterAgent**: Responsible for understanding the folder structure of the project and breaking down the analysis into smaller tasks.
2. **SummarizerAgent**: Focuses on summarizing the content within assigned sections and feeding results back into the system.
3. **GitHubRepoAnalyzer**: Manages the overall analysis process and handles question-answering functionality.
4. **AnalyzerGUI**: Provides a graphical user interface for interacting with the analyzer.

## How It Works

1. The user enters a GitHub repository URL in the GUI.
2. The system analyzes the repository structure using the RouterAgent.
3. SummarizerAgents are deployed to create summaries of specific sections.
4. The results are aggregated into a comprehensive analysis.
5. Users can then ask questions about the repository, which are answered based on the analysis.

## Requirements

- Python 3.7+
- tkinter
- requests
- BeautifulSoup
- PyGithub
- Custom LLM interface (LlamaInterface)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/github-repo-analyzer.git
   ```
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the main script:
   ```
   python main.py
   ```
2. Enter a GitHub repository URL in the provided field.
3. Click "Analyze Repository" to start the analysis process.
4. Once the analysis is complete, you can ask questions about the repository using the question input field.

## Future Improvements

- Implement authentication for GitHub API to increase rate limits
- Add support for analyzing private repositories
- Improve error handling and user feedback
- Enhance the question-answering capabilities with more advanced NLP techniques

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.