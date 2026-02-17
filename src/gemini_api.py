from google import genai
from dotenv import load_dotenv # for hiding api key 
import os #for hiding api
from .utils import load_schema

load_dotenv()
my_api_key = os.getenv("GEMINI_API_KEY") 

client = genai.Client(api_key = my_api_key )


def prompt_gemini(prompt: str, schema_name:str | None = None):  #|None = None is a type hint

    config = {"response_mime_type": "application/json"}

    
    if schema_name:
        schema_json = load_schema(schema_name)
        config["response_schema"] = schema_json



    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config=config

    )
    return response.parsed #returns it as a dictionary 

