from smolagents import (
    InferenceClientModel,
    DuckDuckGoSearchTool,
    CodeAgent
)

# from huggingface_hub import login

model  = InferenceClientModel() # Qwen/Qwen2.5-Coder-32B-Instruct

agent = CodeAgent(
    tools=[DuckDuckGoSearchTool()], # it only needs to code to perform data analysis
    model=model
)

episodes = agent.run(
    task="Search for the top episode recommendations for The Office Series where Dwight Schrute is the protagonist.",
)

for episode in episodes:
    print(episode)

# Product Recall (Season 3, Episode 23)
# Identity Theft Is Not a Joke, Jim! (Season 3, Episode 10)
# Women's Appreciation (Season 3, Episode 23)
# Michael's Last Resort (Season 3, Episode 10)
# Drug Testing (Season 3, Episode 20)

# runtime 20 sec

# dev time 60 mins