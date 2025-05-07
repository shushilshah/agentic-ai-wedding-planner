# import json
# from schema import WeddingPlanningState
# from langchain.tools import tool
# from langchain.chat_models import ChatOpenAI
# from langchain.prompts import PromptTemplate
# import re
# from dotenv import load_dotenv
# load_dotenv()

# llm = ChatOpenAI(model='gpt-4', temperature=0.3)


# def parse_response(state: WeddingPlanningState) -> WeddingPlanningState:
#     raw_responses = state["contact_results"]
#     parsed = []
#     for response in raw_responses:
#         prompt = f"""
# Extract venue info in JSON:
# Message:
# {response}

# Fields: name, location, capacity, pricing, services (list), restrictions
# """
#         try:
#             result = llm.predict(prompt)
#             parsed.append(json.loads(result))
#         except Exception:
#             parsed.append({"error": "Parse failed", "raw": response})
#     return {**state, "parsed_data": parsed}


from schema import WeddingPlanningState
from langchain_openai import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field, ConfigDict
from typing import List
from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# Initialize LLM
# api_key = os.getenv("OPENAI_API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0.3)

# Define the Pydantic model


class VenueInfo(BaseModel):
    name: str = Field(description="Venue name")
    location: str = Field(description="City or region")
    capacity: int = Field(description="Maximum guest capacity")
    pricing: str = Field(description="Pricing details")
    services: List[str] = Field(description="Included services")
    restrictions: str = Field(description="Any restrictions or limitations")

    model_config = ConfigDict(from_attributes=True)


# Create a parser using the correct parser class
parser = PydanticOutputParser(pydantic_object=VenueInfo)

# Define the prompt
prompt_template = ChatPromptTemplate.from_template("""
You are an assistant that extracts structured data about wedding venues. And always return location and restrictions as strings. If not avaialable , set to "unknown" or "None".

Extract the following fields:
- name
- location
- capacity
- pricing
- services (as a list)
- restrictions

Output your answer in JSON format as shown below:
{format_instructions}

Message:
---
{message}
---
""")

# Define the parsing function


def parse_response(state: WeddingPlanningState) -> WeddingPlanningState:
    raw_responses = state["contact_results"]
    parsed = []

    for response in raw_responses:
        try:
            prompt = prompt_template.format_messages(
                message=response,
                format_instructions=parser.get_format_instructions()
            )
            output = llm(prompt)
            # print("MODEL RAW OUTPUT:", output.content)
            parsed_data = parser.parse(output.content)
            parsed.append(parsed_data.dict())
        except Exception as e:
            parsed.append({
                "error": "Parse failed",
                "raw": response,
                "exception": str(e)
            })

    return {**state, "parsed_data": parsed}
