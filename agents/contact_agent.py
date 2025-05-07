from schema import WeddingPlanningState
from langchain.tools import tool
from utils.email_tools import send_email_to_venue


def contact_venue(state: WeddingPlanningState) -> WeddingPlanningState:
    urls = state["urls"]
    results = []
    for url in urls:
        venue_name = url.split("/")[-1].replace("-", " ").title()
        response = send_email_to_venue(
            "venue@example.com", venue_name, "What is your capacity and pricing?")
        results.append(response)
    return {**state, "contact_results": results}
