from concurrent.futures import ThreadPoolExecutor
from utils.utils import llm_call, extract_xml
from typing import List, Dict, Callable

def chain(input: str, prompts: List[str]):
    """Chain multiple LLM calls sequentially passing results between steps

    input --> [LLM1] --> result1 --> [LLM2] --> result2 --> ... --> response to user"""
    result = input
    for i, prompt in enumerate(prompts, start=1):
        print(f"\n Step {i}:")
        result = llm_call(prompt=f"{prompt}\nInput: {result}")
        print(result)
    
    return result

def parallel(prompt: str, inputs: List[str], n_workers: int = 3) -> List[str]:
    """Process multiple inputs concurrently with the same prompt (???)"""
    with ThreadPoolExecutor(max_workers=n_workers) as executor:
        futures = [executor.submit(llm_call,f"{prompt}\nInput: {x}") for x in inputs]
        return [f.result() for f in futures]
    

def route(input: str, routes: Dict[str, str]) -> str:
    """Route inputs to specialized prompts using content classification"""
    print(f"\nAvailable routes: {list(routes.keys)}")
    selector_prompt = f"""
    Analyze the input and select the most appropriate support team from these options: {list(routes.keys())}
    First explain your reasoning, then provide your selection in this XML format:

    <reasoning>
    Brief explanation of why this ticket should be routed to a specific team.
    Consider key terms, user intent, and urgency level.
    </reasoning>

    <selection>
    The chosen team name
    </selection>

    Input: {input}"""

    route_response = llm_call(prompt=selector_prompt)
    reasoning = extract_xml(text = route_response, tag="reasoning")
    route_key = extract_xml(text= route_response, tag="selection").strip().lower()

    print("Routing Analysis: ")
    print(reasoning)
    print(f"\nSelected routes: {route_key}")

    # Process input with selected specialized prompts
    selected_prompt = routes[route_key]

