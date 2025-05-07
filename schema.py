# schema.py
from typing import TypedDict, Optional, List


class WeddingPlanningState(TypedDict):
    query: str
    urls: Optional[List[str]]
    contact_results: Optional[List[str]]
    parsed_data: Optional[List[dict]]
    verified_data: Optional[List[dict]]
    stored: Optional[bool]
