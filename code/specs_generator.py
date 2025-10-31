from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import List, Dict
import dotenv
import os
import json
import pandas as pd

dotenv.load_dotenv()

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
PROJECT_ROOT = os.environ["PROJECT_ROOT"]
MODEL_CHECKPOINT = "gemini-2.5-flash"

class AircraftSpecs(BaseModel):

    aircraft_name: str = Field(default=None, description="Name and model of the aircraft")
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
                           


def aircraft_specs(img_path: str) -> types.GenerateContentResponse:
    img_mime_type = "image/jpeg"

    with open(img_path, 'rb') as f:
        img_bytes = f.read()

    client = genai.Client(
        api_key=GEMINI_API_KEY,
        http_options=types.HttpOptions(api_version="v1alpha")
    )

    ############## STEP 1: SEARCH ##############

    websearch_tool = types.Tool(
        google_search=types.GoogleSearch()
    )

    SEARCH_SYSTEM_INSTRUCTION = """You are an expert aircraft identification and research assistant.
            Use Google Search to find accurate specifications."""

    search_config = types.GenerateContentConfig(
            system_instruction=SEARCH_SYSTEM_INSTRUCTION,
            temperature=0,
            tools=[websearch_tool]
    )

    search_contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_bytes(
                    data=img_bytes,
                    mime_type=img_mime_type
                ),
                types.Part.from_text(
                    text="""Identify this fighter jet from the image and search for its complete specifications.
                    Please provide the following information:
                    - Aircraft name and model
                    - Crew: Number of crew members
                    - Length in meters
                    - Wingspan in meters
                    - Height in meters
                    - Maximum takeoff weight in kilograms
                    - Maximum speed in km/h
                    - Ferry range in kilometers
                    - Service ceiling in meters
                    - G-force limit
                    - Thrust to weight ratio

                    Use Google Search to find accurate and official specifications. Provide detailed information."""
                )
            ]
        )
    ]

    search_response = client.models.generate_content(
        model=MODEL_CHECKPOINT,
        contents=search_contents,
        config=search_config
    )

    ############## STEP 2: STRUCTURED OUTPUT ##############

    STRUCTURE_SYSTEM_INSTRUCTION = """You are a data structuring assistant. 
            Extract the aircraft specifications from the provided text and format them into the exact JSON schema.
            Convert all units to the specified format. If a value is not available, use null."""

    structure_config = types.GenerateContentConfig(
        system_instruction=STRUCTURE_SYSTEM_INSTRUCTION,
        temperature=0,
        response_mime_type='application/json',
        response_schema=AircraftSpecs
    )

    structure_contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(
                    text=f"""Extract and structure the following aircraft information into the JSON schema:
                    
                    {search_response}

                    Requirements:
                    - All lengths in meters
                    - Weight in kilograms
                    - Speed in km/h
                    - Use null for unavailable values
                    - Ensure numerical accuracy"""
                )
            ]
        )
    ]

    structure_response = client.models.generate_content(
        model=MODEL_CHECKPOINT,
        contents=structure_contents,
        config=structure_config
    )

    return structure_response

if __name__ == "__main__":

    img_dir = os.path.join(PROJECT_ROOT, "images")
    img_files = [
        f for f in os.listdir(img_dir)
    ]

    result: List[Dict] = []
    
    # Process each image iteratively
    for img_file in img_files:
        img_path = os.path.join(img_dir, img_file)
        response = aircraft_specs(img_path=img_path)
        specs_dict = json.loads(response.text)

        specs_dict["image_file"] = img_file
        result.append(specs_dict)
    
    # save results in dataframe
    df = pd.DataFrame(result)
    # Reorder columns
    column_order = [
        'image_file',
        'aircraft_name',
        'crew',
        'length',
        'wingspan',
        'height',
        'max_takeoff_weight',
        'max_speed',
        'ferry_range',
        'service_ceiling',
        'g_limit',
        'thrust_weight'
    ]

    column_order = [col for col in column_order if col in df.columns]
    df = df[column_order]

    print(df)

    df.to_csv(path_or_buf="aircraft_specs.csv", index=False)