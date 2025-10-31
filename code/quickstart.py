from google import genai
from google.genai import types

import dotenv
import os

dotenv.load_dotenv()
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
MODEL_CHECKPOINT = "gemini-2.0-flash-lite"

####################### CREATE CLIENT ####################

client = genai.Client(
    api_key=GEMINI_API_KEY,
    http_options=types.HttpOptions(api_version="v1alpha") # this is the stable endpoint.
    # by default SDK uses the beta API endpoints to support preview features.
)

####################### GENERATE CONTENT ####################
################### with text content

# contents = "Who are the members of Swedish House Mafia?"
# response = client.models.generate_content(
#     model=MODEL_CHECKPOINT,
#     contents=contents
# )
# print(response.text)

# contents = "Was Eric Prydz ever associated with Swedish House Mafia?"
# response = client.models.generate_content(
#     model=MODEL_CHECKPOINT,
#     contents = contents
# )
# print(response.text)

################### with uploaded file

# file = client.files.upload(file="a11.txt")


# response = client.models.generate_content(
#     model=MODEL_CHECKPOINT,
#     contents=["Summarize this file: ", file]
# )
# print("\n", response.text)

######## file operations

# print("Listing available files:\n")
# pager = client.files.list(config={'page_size': '10'})

# for uploaded_file in pager.page:
#     print("Name: ", uploaded_file.name)
#     print("Display Name:", uploaded_file.display_name)
#     print("MIME type: ", uploaded_file.mime_type)
#     print("Expiration time", uploaded_file.expiration_time)
#     print("Size in Kb: ", uploaded_file.size_bytes / 1024)

# client.files.delete(name="files/monex3xh0qv3")
# client.files.delete(name="files/5nil62exw4gw")

################### structure the contents
# previously I provided contents as a string (line 22 and line 29) or a list of strings (line 43)
# input contents can be a combination of: string, list of string, function call, list of function calls

# line 23 (and line 29) can be provided to the model using list[types.Content] instance
contents = [
    types.Content(
    role="user", # Must be either 'user' or 'model'
    parts=[types.Part.from_text(text="Why did the chicken cross the road?")]
    )
]