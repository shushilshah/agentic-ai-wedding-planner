from langchain.tools import tool
from utils.scrapper_tools import search_german_venues


# agents/discovery_agent.py
from schema import WeddingPlanningState


def discover_venues(state: WeddingPlanningState) -> WeddingPlanningState:
    query = state["query"]
    # Simulate discovery
    urls = [
        "https://mockvenue.com/berlin-castle",
        "https://mockvenue.com/frankfurt-vineyard",
        "https://mockvenue.com/lakeview-hall"
    ]
    return {**state, "urls": urls}
