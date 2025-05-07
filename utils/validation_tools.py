def cross_validate_venue(venue_data):
    required = ["name", "location", "capacity", "pricing", "services"]
    is_valid = all(venue_data.get(field) for field in required)
    return is_valid, "All required fields present" if is_valid else "Missing critical fields"
