# Data analyst agent
## prepare an agent to carry out a data analyst project end to end
## agent will code its way through the process (Code agent)
## The agent will use already installed libraries to generate code for data analysis on the fly.
## link: https://huggingface.co/learn/cookbook/en/agent_data_analyst

from smolagents import (
    LiteLLMModel, ## example uses InferenceClientModel instead
    CodeAgent
)

# from huggingface_hub import login

model  = LiteLLMModel(
    model_id="ollama/llama3.2:latest",
    api_base="http://127.0.0.1:11434",
    flatten_messages_as_text=False,
    temperature=0.5
)

agent = CodeAgent(
    tools=[], # it only needs to code to perform data analysis
    model=model,
    additional_authorized_imports=["numpy", "pandas", "matplotlib.pyplot", "seaborn"], # to let it use data science-related libraries
    # executor_type="e2b" # safer to use sandbox
)

additional_notes = open("data/california-housing/data_description.txt","r").read()

analysis = agent.run(
    task="""You are an expert data analyst.
    Please load the source file and analyze its content.
    According to the variables you have, begin by listing 3 interesting questions that could be asked on this data, for instance about specific correlations with house price.
    Then answer these questions one by one, by finding the relevant numbers.
    Meanwhile, plot some figures using matplotlib/seaborn and save them to the (already existing) folder './figures/': take care to clear each figure with plt.clf() before doing another plot.

    In your final answer: summarize these correlations and trends
    After each number derive real worlds insights, for instance: "Correlation between is_december and boredness is 1.3453, which suggest people are more bored in winter".
    Your final answer should have at least 3 numbered and detailed parts.
    """,
    additional_args=dict(additional_notes=additional_notes, source_file="data/california-housing/train.csv"),
)

print(analysis)
