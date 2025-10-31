from google import genai
from google.genai import types
from pydantic import BaseModel, Field
import dotenv
import os


class AircraftSpecs(BaseModel):
    # General characteristics
    crew: int = Field(default=1, description="""Number of crew members in the cockpit""")
    length: float = Field(default=None, description="""Length of the aircraft measured from nosetip to tail""", decimal_places=2)
    wingspan: float = Field(default=None, description="""Measurement between both wingtips of the aircraft""", decimal_places=2)
    height: float = Field(default=None, description="""Height measured from the belly to the tail tip""", decimal_places=2)
    max_takeoff_weight: float = Field(default=None, description=""""Maximum allowed takeoff weight""", decimal_places=2)

    # Performance characteristics
    max_speed: float = Field(default=None, description="""Maximum allowed speed """, decimal_places=2)
    ferry_range: float = Field(default=None, description="""Maximum ferry range with or without drop tanks if not supported""", decimal_places=2)
    service_ceiling: float = Field(default=None, description="""Maximum altitude acheived""", decimal_places=2)
    g_limit: float = Field(default=None, description="""Maximum g force tolerated by fuselage""", decimal_places=2)
    thrust_weight: float = Field(default=None, description="""Thrust to weight ratio measured with empty weight""", decimal_places=2)
                           


dotenv.load_dotenv()

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
MODEL_CHECKPOINT = "gemini-2.5-flash"

# img = "images/MIG29K.jpg"
img = "images/TejasALCA.jpg"
img_mime_type = "image/jpeg"

with open(img, 'rb') as f:
    img_bytes = f.read()

client = genai.Client(
    api_key=GEMINI_API_KEY,
    http_options=types.HttpOptions(api_version="v1alpha")
)

# TODO: Wikipedia langchain wrapper tryout

contents = [
    types.Content(
        role="user",
        parts=[
            types.Part.from_bytes(
                data=img_bytes,
                mime_type=img_mime_type
            ),
            types.Part.from_text(text="Identify the fighter jet manufacturer and model in the image")
        ]
    )
]

response = client.models.generate_content(
    model=MODEL_CHECKPOINT,
    contents=contents
)

print(response.text)