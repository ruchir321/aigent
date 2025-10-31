from google import genai
from google.genai import types
from pydantic import BaseModel, Field
import dotenv
import os


class AircraftSpecs(BaseModel):
    # General characteristics
    crew: int = Field(default=1, description="""Number of crew members in the cockpit""")
    length: float = Field(default=None, description="""Length in meters of the aircraft measured from nosetip to tail""")
    wingspan: float = Field(default=None, description="""Measurement in meters between both wingtips of the aircraft""")
    height: float = Field(default=None, description="""Height in meters measured from the belly to the tail tip""")
    max_takeoff_weight: float = Field(default=None, description=""""Maximum allowed takeoff weight in kilograms""")

    # Performance characteristics
    max_speed: float = Field(default=None, description="""Maximum allowed speed in km/h""")
    ferry_range: float = Field(default=None, description="""Maximum ferry range in kilometers with or without drop tanks if not supported""")
    service_ceiling: float = Field(default=None, description="""Maximum altitude acheived in meters""")
    g_limit: float = Field(default=None, description="""Maximum g force tolerated by fuselage""")
    thrust_weight: float = Field(default=None, description="""Thrust to weight ratio measured with empty weight""")
                           


dotenv.load_dotenv()

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
MODEL_CHECKPOINT = "gemini-2.5-flash"
SYSTEM_INSTRUCTION = "You are an information retrieval tool meant to populate the fields of AircraftSpecs class with the help of Google Search. You are not allowed to respond with sentences, only structured output is allowed."

# img = "images/MIG29K.jpg"
img = "images/RafaleB.jpg"
img_mime_type = "image/jpeg"

with open(img, 'rb') as f:
    img_bytes = f.read()

client = genai.Client(
    api_key=GEMINI_API_KEY,
    http_options=types.HttpOptions(api_version="v1alpha")
)

websearch_tool = types.Tool(
    google_search=types.GoogleSearch()
)

config = types.GenerateContentConfig(
    system_instruction=SYSTEM_INSTRUCTION,
    temperature=0,
    tools=[websearch_tool],
    response_mime_type='application/json',
    response_schema=AircraftSpecs
)

contents = [
    types.Content(
        role="user",
        parts=[
            types.Part.from_bytes(
                data=img_bytes,
                mime_type=img_mime_type
            ),
            types.Part.from_text(text="Identify the fighter jet and give me the required information.")
        ]
    )
]

response = client.models.generate_content(
    model=MODEL_CHECKPOINT,
    contents=contents,
    config=config
)

print(response.text)