from langchain.tools import tool
from utils.validation_tools import cross_validate_venue
from schema import WeddingPlanningState


def verify_data(state: WeddingPlanningState) -> WeddingPlanningState:
    parsed_data = state["parsed_data"]
    verified = []
    for item in parsed_data:
        is_valid, notes = cross_validate_venue(item)
        item["verified"] = is_valid
        item["verification_notes"] = notes
        verified.append(item)
    return {**state, "verified_data": verified}
