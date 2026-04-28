import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("Error: OPENAI_API_KEY not found in .env file.")
    exit()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=api_key)

search_tool = DuckDuckGoSearchRun()


@tool
def find_local_notes(topic: str):
    """Searches the computer for a folder matching the user's specific topic."""
    base_path = Path.cwd()

    for root, dirs, files in os.walk(base_path):
        for d in dirs:
            if topic.lower() in d.lower():
                return f"MATCH: Found your local folder for '{topic}' at: {os.path.join(root, d)}"

    return f"No local notes found for '{topic}' in the project directory."

tools = [search_tool, find_local_notes]
llm_with_tools = llm.bind_tools(tools)

def run_assistant(user_query: str):
    messages = [
        SystemMessage(
            content="You are a helpful study assistant. Use find_local_notes for local files and duckduckgo_search for web links."),
        HumanMessage(content=user_query)
    ]

    ai_msg = llm_with_tools.invoke(messages)

    if ai_msg.tool_calls:
        messages.append(ai_msg)
        for tool_call in ai_msg.tool_calls:
            # Map the tools dynamically
            tool_map = {"duckduckgo_search": search_tool, "find_local_notes": find_local_notes}
            selected_tool = tool_map[tool_call["name"]]

            # Execute the tool
            result = selected_tool.invoke(tool_call["args"])
            messages.append({"role": "tool", "tool_call_id": tool_call["id"], "content": str(result)})

        final_answer = llm_with_tools.invoke(messages)
        return final_answer.content

    return ai_msg.content

if __name__ == "__main__":
    print("\n==============================================")
    print("   GENERIC STUDY ASSISTANT IS NOW ONLINE")
    print("==============================================")

    while True:
        # This is where the magic happens: it asks YOU for the input
        user_prompt = input("\nWhat would you like to study or find? (Type 'exit' to stop): ")

        if user_prompt.lower() == 'exit':
            print("Goodbye! Good luck with your project.")
            break

        try:
            print("Searching...")
            response = run_assistant(user_prompt)
            print(f"\nAI ASSISTANT: {response}")
        except Exception as e:
            print(f"An error occurred: {e}")
