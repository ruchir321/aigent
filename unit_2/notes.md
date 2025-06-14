# smolagent

types of agents:

* code agent: for SDE tasks
* tool calling agent: for creating modular/function driven workflow execution
* retrieval agent: for accessing and synthesizing information

**agent**: Program that uses LLM to `think` based on `observations` and `act` on the thinking.

## advantages of smolagent framework

1. abstraction for simplicity
2. Code Agents write and execute code for you
3. freedom to use LLM's with HF API
4. Integration with HF spaces and Hub

## LLM's options

choose from a list of LLM implementations:

1. `TransformerModel`: implement a `transformers` `pipeline`
2. `InferenceClientModel`: serverless interface with third party inference providers on HF Hub
3. `LiteLLMModel`: uses `LiteLLM` for lightweight model interactions
4. `OpenAIServerModel`: use any service which provides an OpenAI API interface
5. `AzureOpenAIServerModel`: integrate with Azure OpenAI deployment

`MultiStepAgent`:

1. performs one thought -> one tool call and execution
2. it is an abstraction of `ReAct` framework
3. Every agent in `smolagents` implements `MultiStepAgent`

`MultiStepAgent` is different than `MultiAgent`

`MultiAgent` is a workflow where one `MultiStepAgent` can trigger another `MultiStepAgent`

### Code Agents

Agents that use code to take actions.

[CodeAct](https://arxiv.org/pdf/2402.01030) og paper: integrates fine tuned Llama2 and Mistral LLM with python interpreter to write code on the fly

Earlier agents acted on Text or JSON format which specifies tool name and arguements, which the system must parse to determine which tool to use
