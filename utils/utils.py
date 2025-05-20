import re
import dotenv
import os
from ollama import Client, chat, list

dotenv.load_dotenv()

os.environ["LANGSMITH_API_KEY"] = dotenv.dotenv_values()["LANGSMITH_API_KEY"]
os.environ["LANGSMITH_TRACING"] = dotenv.dotenv_values()["LANGSMITH_TRACING"]
os.environ["LANGSMITH_PROJECT"] = dotenv.dotenv_values()["LANGSMITH_PROJECT"]

client = Client(host="http://localhost:11434")

def llm_call(prompt: str, system_prompt: str = "", model="gemma3:4b") -> str:
    """
    Calls the model with the given prompt and returns the response
    """
    messages = [
        {
            "role": "user",
            "content": prompt
        },
        {
            "role": "system",
            "content": system_prompt
        }
    ]
    # print (list())

    response = chat(
        model=model,
        messages=messages,
        options={
            # "num_keep": 5,
            # "seed": 42,
            # "num_predict": 100,
            # "top_k": 20,
            # "top_p": 0.9,
            # "min_p": 0.0,
            # "typical_p": 0.7,
            # "repeat_last_n": 33,
            "temperature": 0.1
            # "repeat_penalty": 1.2,
            # "presence_penalty": 1.5,
            # "frequency_penalty": 1.0,
            # "mirostat": 1,
            # "mirostat_tau": 0.8,
            # "mirostat_eta": 0.6,
            # "penalize_newline": True,
            # "stop": ["\n", "user:"],
            # "numa": False,
            # "num_ctx": 1024,
            # "num_batch": 2,
            # "num_gpu": 1,
            # "main_gpu": 0,
            # "low_vram": False,
            # "vocab_only": False,
            # "use_mmap": True,
            # "use_mlock": False,
            # "num_thread": 8
        }
    )

    return response

def extract_xml(text: str, tag: str) -> str:
    """
    Extracts content of specified tags, used to parse structured outputs
    
    Args:
        text(str): The test containing the XML
        tag(str): The XML tag to be used to extract content from
    
    Returns:
        str: The content of a given XML tag, or empty if tag is not found
    """

    match = re.match(f"<{tag}>(.*?)</{tag}>", text, re.DOTALL)
    return match.group(group=1) if match else ""

