
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

<img width="318" height="702" alt="download" src="https://github.com/user-attachments/assets/b823d693-cc9d-4462-b569-94ad5fe46b1a" />


## ✨ Features

* **Multi-Agent Collaboration**: Utilizes multiple specialized agents (nodes) working in concert.
* **Self-Correction**: Implements a reflective loop where one agent critiques another, progressively improving the output quality.
* **Real-Time Web Research**: Integrated with `TavilySearch` for up-to-date information.
* **Modular Architecture**: Cleanly separated logic into `state.py`, `tools.py`, `nodes.py`, and `workflow.py` for easy maintenance and extension.
* **Final Document Generation**: Automatically saves the final report as a `.docx` file using `python-docx`.

## 🛠️ Tech Stack

* **LangGraph**: The core library for building stateful, multi-agent applications.
* **LangChain**: For core abstractions and tool integration.
* **Google Gemini**: The Large Language Model used by the agents (via `langchain-google-genai`).
* **Tavily AI**: For the web search tool (`langchain-tavily`).
* **Python `dotenv`**: For managing API keys.
* **`python-docx`**: For creating the final Word document.

## 📂 Project Structure


```bash
/homework_agent
├── main.ipynb                                      # Main notebook to run the agent
├── workflow.py                                     # Defines the StateGraph, nodes, and edges
├── nodes.py                                        # Contains the functions for each agent (Researcher, Writer, etc.)
├── tools.py                                        # Initializes tools (e.g., TavilySearch)
├── student_number_homeworkname.docx                # An example result
└── student_number_homeworkname2.docx               # An example result

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
