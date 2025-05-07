from langgraph.graph import StateGraph
from langchain_community.chat_models import ChatOpenAI
from agents.discovery_agent import discover_venues
from agents.contact_agent import contact_venue
from agents.parse_response_agent import parse_response
from agents.verification_agent import verify_data
from agents.store_agent import store_venue_data
from dotenv import load_dotenv
from typing import TypedDict, Optional, List
from schema import WeddingPlanningState
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0.3)

graph = StateGraph(WeddingPlanningState)

graph.add_node("discovery", discover_venues)
graph.add_node("contact", contact_venue)
graph.add_node("parse_response", parse_response)
graph.add_node("verify", verify_data)
graph.add_node("store", store_venue_data)


# Define edges(flow)
graph.set_entry_point("discovery")
graph.add_edge("discovery", "contact")
graph.add_edge("contact", "parse_response")
graph.add_edge("parse_response", "verify")
graph.add_edge("verify", "store")


# End after storing
graph.set_finish_point("store")

# Compile and run
workflow = graph.compile()

if __name__ == "__main__":
    input_query = {"query": "wedding venues in Berlin"}
    result = workflow.invoke(input_query)
    print(result)
