# tools.py
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_experimental.tools import PythonREPLTool

# Initialize the search tool
# name parameter is important for the agent to identify the tool
search_tool = DuckDuckGoSearchRun(name="WebSearch")

# Initialize the Python REPL tool
# This provides the agent the ability to execute Python code
python_repl_tool = PythonREPLTool()

# Create a list of tools that the agent can use
# Now includes both WebSearch and PythonREPL
agent_tools = [search_tool, python_repl_tool]

# You can add more tools here later and append them to the agent_tools list
# from langchain.tools import ...
# my_other_tool = ...
# agent_tools.append(my_other_tool)