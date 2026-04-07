import os
import sys
from pathlib import Path

import google.generativeai as genai
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools import google_search, tool


# --- 1. Environment and API Key Setup ---
print("STATUS: Loading .env file...")
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    print("FATAL ERROR: GEMINI_API_KEY environment variable not found.")
    print("Please check your .env file and ensure it is in the same directory.")
    sys.exit(1)

# Configure Gemini SDK with the loaded API key.
genai.configure(api_key=api_key)
print("STATUS: API Key Loaded. ADK successfully configured.")


# --- 2. Custom Tool Definition (Feature: Custom Tool) ---
@tool
def save_content_tool(filename: str, content: str) -> str:
    """
    Saves the given content to a text file.

    Args:
        filename: The name of the file (e.g., 'summary.txt').
        content: The text content to save.

    Returns:
        A string confirming the save.
    """
    try:
        safe_filename = Path(filename).name
        if not safe_filename.endswith(".txt"):
            safe_filename = f"{safe_filename}.txt"

        with open(safe_filename, "w", encoding="utf-8") as file_handle:
            file_handle.write(content)

        tool_output = f"Successfully saved content to {safe_filename}"
        print(f"\n[Tool Called]: save_content_tool -> {tool_output}\n")
        return tool_output
    except Exception as exc:
        error_message = f"Error saving file: {exc}"
        print(f"\n[Tool Error]: {error_message}\n")
        return error_message


# --- 3. Agent Definitions (Feature: Multi-agent System) ---
print("STATUS: Defining agents...")

research_agent = Agent(
    model="models/gemini-1.5-flash",
    instruction=(
        "You are a world-class researcher. Your job is to find the most "
        "relevant and detailed information about a user's query using the "
        "google_search tool. Provide a comprehensive text block of your findings."
    ),
    tools=[google_search],
)

writer_agent = Agent(
    model="models/gemini-1.5-pro-latest",
    instruction=(
        "You are an expert summarizer and writer. Take the provided research "
        "text and create a concise, 3-bullet-point summary. After summarizing, "
        "you MUST use the save_content_tool to save this summary to the filename "
        "specified by the user."
    ),
    tools=[save_content_tool],
)

print("STATUS: Agents defined successfully.")


# --- 4. Main Execution Logic (Sequential Flow) ---
def run_agent_pipeline(user_query: str, output_filename: str) -> None:
    """Runs the sequential agent pipeline: Research -> Summarize -> Save."""
    try:
        print("\n--- 1. Starting Research Agent ---")
        print(f"Query: {user_query}")

        research_result = research_agent.chat(user_query)
        research_text = getattr(research_result, "text", "")
        if not research_text:
            raise RuntimeError("Research agent returned empty output.")

        print("STATUS: Research complete.")

        print("\n--- 2. Starting Writer Agent ---")
        summary_prompt = f"""
Please summarize the following research text and save it using the filename:
'{output_filename}'.

Research Text:
{research_text}
"""

        summary_result = writer_agent.chat(summary_prompt)
        print("STATUS: Summarization and save complete.")
        print(f"Final Output: {getattr(summary_result, 'text', '')}")

        print("\n--- Pipeline Finished Successfully ---")
        print(f"Check the '{output_filename}' file in your folder.")

    except Exception as exc:
        print("\n--- ERROR IN PIPELINE ---")
        print(f"An error occurred: {exc}")
        print("Please check your API key, internet, and tool permissions.")


# --- 5. Run the code ---
if __name__ == "__main__":
    query_topic = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "What are the key features of Google's ADK (Agent Development Kit)?"
    )
    output_file = sys.argv[2] if len(sys.argv) > 2 else "adk_summary.txt"

    run_agent_pipeline(query_topic, output_file)
