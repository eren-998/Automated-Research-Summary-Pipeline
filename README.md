# Automated Research & Summary Pipeline

**Capstone project for the Kaggle 5-Day AI Agents Intensive (Google).**
This repository contains the source code for a sequential multi-agent system built with the Google Agent Development Kit (ADK).

---

### Problem Statement
In today's fast-paced digital world, the **"time-to-insight" ratio is critical**. Professionals—from market analysts and content creators to academic researchers—spend countless hours on the repetitive, low-value task of manual web research.

This process involves:
1.  Manually Googling a topic.
2.  Sifting through dozens of irrelevant links.
3.  Reading multiple sources to extract key points.
4.  Painstakingly summarizing the findings.

This manual bottleneck is not just tedious; it's **inefficient, expensive (in terms of billable hours), and prone to human error**. It's an important problem because it directly impacts productivity and prevents experts from focusing on what truly matters: **high-level analysis and decision-making**.

---
### Why agents?
This problem is too complex for a simple script but perfect for AI Agents. A simple script can't handle the ambiguity of web searches or the nuanced task of summarization.

**Agents are the right solution because they are autonomous, tool-using, and collaborative:**

* **Tool Use:** Agents can be given "tools" to interact with the real world. In this case, we gave one agent the **`Google Search`** tool to access live web data, and another a **custom `save_summary_tool`** to interact with the file system.
* **Task Decomposition:** We can break the complex problem (research *and* summarize) into smaller, manageable tasks and assign specialized agents to each one (a `ResearchAgent` and a `SummarizerAgent`).
* **Sequential Reasoning (A2A):** The agents can work *sequentially*. The `SummarizerAgent` doesn't just get a prompt; it gets the **direct output** from the `ResearchAgent`. This **Agent-to-Agent (A2A)** communication mimics a real-world assembly line, making the workflow robust and intelligent.

---
### What you created
We created an **Automated Research & Summary Pipeline**, a sequential multi-agent system built with the Google Agent Development Kit (ADK).

The architecture is a clean, two-step data flow:

1.  **Agent 1: `ResearchAgent` (`gemini-1.5-flash` + `Google Search` tool)**
    * **Input:** User's topic (e.g., "What are the key features of Google's ADK?").
    * **Action:** Uses the `Google Search` tool to perform a comprehensive web search.
    * **Output:** A large block of raw text containing all the research findings.

2.  **Agent 2: `SummarizerAgent` (`gemini-1.5-pro` + custom `save_summary_tool`)**
    * **Input:** The raw text output from the `ResearchAgent`.
    * **Action:** Analyzes the text, creates a concise 3-bullet-point summary, and calls the `save_summary_tool` with `summary_output.txt` as the filename.
    * **Output:** A status message confirming the file has been saved (e.g., `Successfully saved summary to summary_output.txt`).

---
### Demo
Here is a demonstration of the agent pipeline in action.

1.  **The Trigger:** The user runs the script with the query: `What are the key features of Google's ADK?`
    ```powershell
    python agent.py
    ```

2.  **The Execution:** The terminal shows the pipeline's real-time status, confirming the API key load and agent definitions.

3.  **Tool Calls (Observability):** We can observe the agents calling their tools in real-time.
    ```bash
    STATUS: API Key Loaded. ADK successfully configured.
    STATUS: Defining agents...
    STATUS: Agents defined successfully.
    
    --- 1. Starting Research Agent ---
    Query: What are the key features of Google's ADK (Agent Development Kit)?
    Research complete.
    
    --- 2. Starting Summarizer Agent ---
    
    [Tool Called]: save_summary_tool -> Successfully saved summary to summary_output.txt
    
    Summarization complete.
    Final Output: The summary has been saved to summary_output.txt.
    
    --- Pipeline Finished Successfully ---
    Check 'summary_output.txt' file in your folder.
    ```

4.  **The Result:** The pipeline finishes, and a new file, `summary_output.txt`, is created in the project folder with the final, summarized content:

    ```text
    Here is a summary of Google's ADK:

    * **Multi-Agent Systems:** The ADK is designed to build complex, multi-agent systems, allowing developers to create sequential, parallel, or looping agent interactions.
    * **Powerful Tool Integration:** It comes with built-in tools like `Google Search` and `code_execution`, and makes it easy to create custom tools (using the `@tool` decorator) or integrate OpenAPI specs.
    * **State & Memory Management:** The ADK provides robust features for managing session state and long-term memory (like MemoryBank), enabling agents to have contextual and persistent conversations.
    ```

---
### The Build
This solution was built using **Python 3** and the **Google Agent Development Kit (ADK)**.

* **Core Library:** `google-adk`
* **Environment:** `python-dotenv` (to securely load the `GEMINI_API_KEY`)
* **Key Features Implemented:**
    1.  **Multi-agent system (Sequential):** Created two `Agent` instances (`ResearchAgent`, `SummarizerAgent`) that pass data from one to the next.
    2.  **Tools (Built-in):** Utilized the pre-built `Google Search` tool.
    3.  **Tools (Custom):** Created a new `save_content_tool` using the `@tool` decorator to interact with the file system.

---
### If I had more time, this is what I'd do
This project provides a strong foundation. With more time, I would focus on scaling and productionalizing the agent:

1.  **Deploy to Cloud Run (Agent Deployment):** I would containerize this Python agent and deploy it to **Google Cloud Run**, turning it into a scalable API endpoint.
2.  **Integrate with n8n (Orchestration):** I would build an n8n workflow to sit on top of the deployed agent. A **Webhook Node** would trigger the workflow, an **HTTP Request Node** would call the agent, and a **Slack/Gmail Node** would send the final `summary_output.txt` to the end-user.
3.  **Add Long-Term Memory (Sessions & Memory):** I would implement the ADK's `MemoryBank` feature to allow the agent to remember past research queries and prevent redundant work.
