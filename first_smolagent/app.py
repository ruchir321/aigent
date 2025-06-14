# first agent framework try out
## tool calling practice: 2 tool functions
## 

from smolagents import (
    CodeAgent # this agent will generate code for tool calls then parse and execute
    , DuckDuckGoSearchTool # web search tool
    , FinalAnswerTool # A tool which generates the final answer (why does an agent need a tool for that??)
    , InferenceClientModel
    , load_tool # Main function to quickly load a tool from the Hub
    , tool # convert custom tool function to an instance of Tool Subclass (Tool Subclass: all the <tool_name>Tool are an instance of Tool subclass)
)

import gradio as gr

import datetime
import requests
import pytz # timezone definitions
import yaml

# Use the exact template for docstring down to the colons and indentation (the docstring parsing is strict)
@tool
def nothing(arg1:str, arg2:str) -> str:
    """A tool that does nothing
    Args:
        arg1: The first arguement
        arg2: The second arguement
    """

    return "Hard in the Paint"

@tool
def get_current_time_in_timezone(timezone:str) -> str:
    """A tool that returns the current timezone in a specific timezone
    Args:
        timezone: valid timezone name(e.g: 'America/Toronto')
    """ 

    try:
        # timezone object
        tz = pytz.timezone(timezone)
        # get time in the timezone
        local_time = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        return f"The current time in {timezone} is: {local_time}"
    except Exception as e:
        return f"Error fetching local time for {timezone}: str(e)"
    

final_answer = FinalAnswerTool()

model = InferenceClientModel(
    model_id="Qwen/Qwen2.5-Coder-32B-Instruct",
    custom_role_conversions=None,
    max_tokens=2096,
    temperature=0.5
)

