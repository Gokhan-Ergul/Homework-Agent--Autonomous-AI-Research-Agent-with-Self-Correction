# Homework-Agent--Autonomous-AI-Research-Agent-with-Self-Correction
This project is an advanced, multi-agent AI system built using **LangGraph**. It's designed to autonomously produce in-depth, high-quality research reports on complex topics.

Unlike a simple chatbot, this system simulates a team of specialized agents:
* **Researcher Agent**: Gathers information from the web using tools (Tavily Search).
* **Writer Agent**: Drafts the content based on the research.
* **Controller Agent**: Critiques the draft, checks for errors, and requests revisions.
* **Formatter Agent**: Formats the final, approved content into a `.docx` document.
* **compile_research_node**: A node that runs after the research loop. It finds all the `ToolMessage` results and gathers their content into the `researcher_result` state key.

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

* **Interactive Web UI**: A user-friendly interface built with **Streamlit** to visualize the agent's progress in real-time.
* **FastAPI Backend**: Robust API architecture separating the agent logic from the user interface.
* **Multi-Agent Collaboration**: Utilizes multiple specialized agents (nodes) working in concert.
* **Self-Correction**: Implements a reflective loop where one agent critiques another, progressively improving the output quality.
* **Advanced RAG Integration**: Employs a sophisticated hybrid retrieval system for deep contextual search.
    * **`BM25Retriever`**: For efficient, keyword-based (sparse) retrieval.
    * **`EnsembleRetriever`**: Combines `BM25` with a semantic vector search (`SimilarityRetriever`).
    * **`MultiQueryRetriever`**: Uses an LLM to generate multiple query variations to improve recall.
* **Hybrid Research**: Dynamically uses both real-time web search (`TavilySearch`) and the private RAG database.
* **Final Document Generation**: Automatically saves the final report as a `.docx` file.
  
## 🛠️ Tech Stack

* **Frontend**: Streamlit (for the interactive Dashboard)
* **Backend**: FastAPI (for the REST API)
* **Core Logic**: LangGraph & LangChain
* **LLM**: Google Gemini (via `langchain-google-genai`)
* **Search**: Tavily AI
* **Vector DB**: ChromaDB / FAISS
* **Utilities**: `python-docx`, `pypdf`, `dotenv`

## 📂 Project Structure


```bash
/homework_agent
├── app/                         # FastAPI backend logic
│   ├── main.py                  # API Entry point
│   └── ...
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
├── frontend.py                            # Streamlit User Interface
├── main.ipynb                             # Main notebook to run the agent
├── workflow.py                            # Defines the StateGraph, nodes, and edges
├── nodes.py                               # Contains the functions for each agent (Researcher, Writer, etc.)
├── tools.py                               # Initializes tools (TavilySearch, RAG retriever)
├── long_research_query.docx               # An example result
└── new_complex_query.docx


```
## 🚀 How to Use

You can run this project via the interactive Web UI or the Jupyter Notebook.

### Option 1: Run the Web Application (Recommended)

1.  **Start the Backend (FastAPI):**
    Open a terminal and run the API server:
    ```bash
    uvicorn app.main:app --reload
    ```

2.  **Start the Frontend (Streamlit):**
    Open a **new** terminal window and run:
    ```bash
    streamlit run frontend.py
    ```

3.  **Research:**
    Open your browser (usually at `http://localhost:8501`). Enter your research topic, and watch the agents work in real-time!

    ![Agent Interface Screenshot](path/to/your/screenshot.png)
    *(Place your screenshot in the folder and update this path)*

### Option 2: Run via Notebook (Dev Mode)

1.  **Launch Jupyter Lab:**
    ```bash
    jupyter lab
    ```
2.  **Open `main.ipynb`** and run the cells to execute the agent programmatically.

4.  **Check the Output:**
    The agent will run for several minutes (this is normal due to the multiple LLM calls and self-correction loops). Once complete, you will find a `.docx` file (e.g., `student_number_homeworkname.docx`) in your directory with the full report.

## 🔮 Future Improvements
* Add a history tab to the Streamlit UI to view past reports.
* Allow users to upload their own PDFs via the UI for the RAG system.
* Dockerize the application for easier deployment.
