from schema import WeddingPlanningState
from langchain.tools import tool
import json
import os

DATASET_PATH = "data/venues.json"


def store_venue_data(state: WeddingPlanningState) -> WeddingPlanningState:
    os.makedirs("data", exist_ok=True)
    verified = state["verified_data"]

    # Load existing
    if os.path.exists(DATASET_PATH):
        with open(DATASET_PATH, "r") as f:
            dataset = json.load(f)
    else:
        dataset = []

    dataset.extend(verified)

    with open(DATASET_PATH, "w") as f:
        json.dump(dataset, f, indent=2)

    return {**state, "stored": True}
