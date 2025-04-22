from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama

from langchain_community.tools.tavily_search.tool import TavilySearchResults
from langchain_community.tools.gmail import GmailSearch

from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

LLM_MODEL = "llama3.2"

import dotenv
import os

dotenv.load_dotenv()

os.environ["LANGSMITH_API_KEY"] = dotenv.dotenv_values()["LANGSMITH_API_KEY"]
os.environ["LANGSMITH_TRACING"] = dotenv.dotenv_values()["LANGSMITH_TRACING"]
os.environ["LANGSMITH_PROJECT"] = dotenv.dotenv_values()["LANGSMITH_PROJECT"]

# create agent
model = ChatOllama(model=LLM_MODEL)

search = TavilySearchResults(
            description=(
                            "A search engine optimized for comprehensive, accurate, and trusted results. "
                            "Useful for when you need to answer questions about current events. "
                            "Input should be a search query."
                        ),
            max_results=2
        )

gmail = GmailSearch(
            description=(
                            "Use this tool to search for email messages or threads."
                            " The input must be a valid Gmail query."
                            " The output is a JSON list of the requested resource."
                        )           
        )

tools = [search, gmail]

memory = MemorySaver()
agent_executor = create_react_agent(model,tools,checkpointer=memory)

# # use the agent
# config = {"configurable": {"thread_id": "abc123"}}
# for step in agent_executor.stream(
#     {"messages": [HumanMessage(content="Hi I'm Drake! I live in Toronto")]},
#     config,
#     stream_mode="values"
# ):
#     step["messages"][-1].pretty_print()

# for step in agent_executor.stream(
#     {"messages": [HumanMessage(content="What is the weather where I live")]},
#     config,
#     stream_mode="values"
# ):
#     step["messages"][-1].pretty_print()

example_query = "Draft an email to fake@fake.com thanking them for coffee."

events = agent_executor.stream(
    {"messages": [("user", example_query)]},
    stream_mode="values",
)
for event in events:
    event["messages"][-1].pretty_print()
