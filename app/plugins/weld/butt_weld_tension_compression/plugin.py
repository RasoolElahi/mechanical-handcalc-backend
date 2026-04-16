"""
Placeholder plugin module for: Butt weld - tension / compression
Add real engineering input models and solver logic here later.
"""

PLUGIN_ID = "weld__butt_weld_tension_compression"
TOP_CATEGORY = "WELD"
SUBCATEGORY = "Butt weld - tension / compression"

def solve(user_name: str, inputs: dict) -> dict:
    return {
        "plugin_id": PLUGIN_ID,
        "user_name": user_name,
        "status": "under_development",
        "message": "This calculation is under development.",
        "inputs": inputs,
    }
