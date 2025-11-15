import os
import sys
import google.ai.generativelanguage as genai
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
    sys.exit(1)  # Exit the script with an error code
else:
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
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        tool_output = f"Successfully saved content to {filename}"
        print(f"\n[Tool Called]: save_content_tool -> {tool_output}\n")
        return tool_output
    except Exception as e:
        error_message = f"Error saving file: {e}"
        print(f"\n[Tool Error]: {error_message}\n")
        return error_message

# --- 3. Agent Definitions (Feature: Multi-agent System) ---

print("STATUS: Defining agents...")

# AGENT 1: The Researcher
# This agent uses a built-in tool (Feature: Built-in Tool)
research_agent = Agent(
    model="models/gemini-1.5-flash",
    instruction="""You are a world-class researcher. 
    Your job is to find the most relevant and detailed information 
    about a user's query using the google_search tool.
    Provide a comprehensive text block of your findings.""",
    tools=[google_search]
)

# AGENT 2: The Summarizer & Writer
# This agent uses our custom tool.
writer_agent = Agent(
    model="models/gemini-1.5-pro-latest",
    instruction="""You are an expert summarizer and writer. 
    Take the provided research text and create a concise, 
    3-bullet-point summary.
    After summarizing, you MUST use the save_content_tool 
    to save this summary to the filename specified by the user.""",
    tools=[save_content_tool]
)

print("STATUS: Agents defined successfully.")

# --- 4. Main Execution Logic (Sequential Flow) ---

def run_agent_pipeline(user_query: str, output_filename: str) -> None:
    """
    Runs the sequential agent pipeline: Research -> Summarize -> Save
    """
    try:
        # Step 1: Call the Research Agent
        print(f"\n--- 1. Starting Research Agent ---")
        print(f"Query: {user_query}")
        
        research_result = research_agent.chat(user_query)
        
        print("STATUS: Research complete.")
        # print(f"Raw Research: {research_result.text[:100]}...") # Optional: uncomment to debug raw text

        # Step 2: Call the Writer Agent
        print("\n--- 2. Starting Writer Agent ---")
        
        # We pass the research output AND the desired filename to the agent
        summary_prompt = f"""
        Please summarize the following research text 
        and save it using the filename: '{output_filename}'.
        
        Research Text:
        {research_result.text}
        """
        
        summary_result = writer_agent.chat(summary_prompt)
        
        print("STATUS: Summarization and save complete.")
        print(f"Final Output: {summary_result.text}")
        
        print("\n--- Pipeline Finished Successfully ---")
        print(f"Check the '{output_filename}' file in your folder.")

    except Exception as e:
        print(f"\n--- ERROR IN PIPELINE ---")
        print(f"An error occurred: {e}")
        print("Please check your API key, internet, and tool permissions.")

# --- 5. Run the code ---
if __name__ == "__main__":
    
    # Define the research topic and the desired output filename
    query_topic = "What are the key features of Google's ADK (Agent Development Kit)?"
    output_file = "adk_summary.txt"
    
    run_agent_pipeline(query_topic, output_file)