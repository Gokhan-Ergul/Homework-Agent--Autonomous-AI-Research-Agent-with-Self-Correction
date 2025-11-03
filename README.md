# Homework-Agent--Autonomous-AI-Research-Agent-with-Self-Correction
This project is an advanced, multi-agent AI system built using **LangGraph**. It's designed to autonomously produce in-depth, high-quality research reports on complex topics.

Unlike a simple chatbot, this system simulates a team of specialized agents:
* **Researcher Agent**: Gathers information from the web using tools (Tavily Search).
* **Writer Agent**: Drafts the content based on the research.
* **Controller Agent**: Critiques the draft, checks for errors, and requests revisions.
* **Formatter Agent**: Formats the final, approved content into a `.docx` document.

The core of this project is its **self-correcting loop**, where the `Writer` and `Controller` agents work iteratively until the report meets a high-quality standard.

## 🤖 Agentic Workflow

The system operates on a state machine defined in `workflow.py`. The flow is as follows:

1.  **Input**: The user provides a complex research topic (e.g., "Write a 500-word report on the future of generative AI in healthcare...").
2.  **Research**: The `Researcher_agent` node is triggered. It uses the `TavilySearch` tool to gather relevant, up-to-date information from the web.
3.  **Compile**: A `compile_research_node` (if you have one) synthesizes the findings.
4.  **Draft**: The `writer_agent` node takes the research and writes the first draft of the report with academic language in markdown.
5.  **Review (The Loop)**:
    * The `controller_agent` node reviews the draft.
    * **If Errors Found**: The `Controller` identifies flaws (e.g., "missing analysis," "too brief," "factual error") and sends the draft back to the `writer_agent` for revision.
    * This "Write -> Review -> Revise" loop continues until the `Controller` approves the draft.
6.  **Format**: The `formatter_node` takes the final approved text and saves it as a `.docx` file.

Here is a simplified diagram of the core self-correction loop:

<img width="378" height="777" alt="download" src="https://github.com/user-attachments/assets/ebf0aeb1-653a-4863-8499-d0ae43caf101" />


## ✨ Features

* **Multi-Agent Collaboration**: Utilizes multiple specialized agents (nodes) working in concert.
* **Self-Correction**: Implements a reflective loop where one agent critiques another, progressively improving the output quality.
* **Advanced RAG Integration**: Employs a sophisticated hybrid retrieval system for deep contextual search.
    * **`BM25Retriever`**: For efficient, keyword-based (sparse) retrieval.
    * **`EnsembleRetriever`**: Combines `BM25` with a semantic vector search (`SimilarityRetriever`) to get the best of both worlds.
    * **`MultiQueryRetriever`**: Uses an LLM to generate multiple query variations, maximizing the chance of finding relevant documents (improving recall).
* **Hybrid Research**: Dynamically uses both real-time web search (`TavilySearch`) and the private RAG database.
* **Modular Architecture**: Cleanly separated logic into  `tools.py`, `nodes.py`, and `workflow.py` for easy maintenance and extension.
* **Final Document Generation**: Automatically saves the final report as a `.docx` file using `python-docx`.
  
## 🛠️ Tech Stack

* **LangGraph**: The core library for building stateful, multi-agent applications.
* **LangChain**: For core abstractions, tool integration, and the RAG pipeline.
* **`langchain-community` / `langchain-classic`**: For specific retrievers like `BM25Retriever` and `EnsembleRetriever`.
* **Google Gemini**: The Large Language Model used by the agents (via `langchain-google-genai`).
* **Tavily AI**: For the web search tool (`langchain-tavily`).
* **Vector Database (e.g., `ChromaDB`, `FAISS`)**: To store and index the RAG documents.
* **`pypdf` (or similar)**: For loading and processing the `.pdf` documents for the RAG database.
* **Python `dotenv`**: For managing API keys.
* **`python-docx`**: For creating the final Word document.

## 📂 Project Structure


```bash
/homework_agent
├── Database_for_RAG/
│   ├── A Review of Prominent Paradigms for LLMBased_Agent_Tool_Use_Including_RAG_Planning_and_Feedback_Learning.pdf
│   ├── A Survey on Large Language Model based Autonomous Agents.pdf
│   ├── A Survey on the Memory Mechanism of Large Language Model based Agents.pdf
│   ├── Augmented Language Models.pdf
│   ├── The Rise and Potential of Large Language Model Based Agents.pdf
│   └── Understanding the planning of LLM agents.pdf
├── output/
   ├── 'memory' means for an LLM agent.docx
   ├── Generative AI in Healthcare.docx
   ├── long_research_query.docx
   ├── new_complex_query.docx
   └── student_number_homeworkname.docx
├── main.ipynb                             # Main notebook to run the agent
├── workflow.py                            # Defines the StateGraph, nodes, and edges
├── nodes.py                               # Contains the functions for each agent (Researcher, Writer, etc.)
├── tools.py                               # Initializes tools (TavilySearch, RAG retriever)
├── long_research_query.docx               # An example result
└── new_complex_query.docx


```
### 3. How to Use

1.  **Launch Jupyter Lab:**
    ```bash
    jupyter lab
    ```


2.  **Open `main.ipynb`:**
    Run the cells in the notebook.

3.  **Provide a Complex Prompt:**
    This agent is designed for complex, multi-step research tasks, not simple questions.

    ❌ **Bad Prompt (Inefficient):**
    ```python
    # This will be very slow and inefficient for such a simple task.
    user_input = HumanMessage(content='10 interview questions about machine learning.')
    ```

    ✅ **Good Prompt (Designed for this system):**
    ```python
    user_input = HumanMessage(
        content="""
        Write a 500-word report on the future of quantum computing.
        1. Start with an introduction to qubits.
        2. Explain at least 2 potential application areas.
        3. Discuss the biggest technical challenges.
        4. Conclude with a summary of its potential impact.
        Use web search to find current information.
        """
    )
    
    response = app.invoke({'messages': [user_input]})
    ```

4.  **Check the Output:**
    The agent will run for several minutes (this is normal due to the multiple LLM calls and self-correction loops). Once complete, you will find a `.docx` file (e.g., `student_number_homeworkname.docx`) in your directory with the full report.

## 🔮 Future Improvements

* **Add RAG**: Integrate a vector database (`ChromaDB`, `FAISS`) to create a `document_search_tool`. This would allow the `Researcher_agent` to choose between searching the web (Tavily) or private documents (RAG).
* **Parallelization**: Modify the graph to run multiple research queries in parallel to speed up the information-gathering phase.

* 
