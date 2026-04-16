
from __future__ import annotations

CATEGORY_PRESETS = {
    "BEAM": [
        {"name": "length", "label": "Length, L", "type": "number", "unit": "in", "default": 10.0, "min": 0.0},
        {"name": "load", "label": "Load", "type": "number", "unit": "lbf", "default": 100.0},
        {"name": "elastic_modulus", "label": "Elastic Modulus, E", "type": "number", "unit": "ksi", "default": 29000.0},
        {"name": "moment_of_inertia", "label": "Moment of Inertia, I", "type": "number", "unit": "in^4", "default": 1.0},
        {"name": "factor_of_safety", "label": "Factor of Safety", "type": "number", "default": 2.0},
    ],
    "BUCKLING": [
        {"name": "length", "label": "Column Length, L", "type": "number", "unit": "in", "default": 20.0, "min": 0.0},
        {"name": "load", "label": "Axial Load", "type": "number", "unit": "lbf", "default": 1000.0},
        {"name": "effective_length_factor", "label": "Effective Length Factor, K", "type": "number", "default": 1.0},
        {"name": "elastic_modulus", "label": "Elastic Modulus, E", "type": "number", "unit": "ksi", "default": 29000.0},
        {"name": "yield_strength", "label": "Yield Strength", "type": "number", "unit": "ksi", "default": 36.0},
        {"name": "area", "label": "Area, A", "type": "number", "unit": "in^2", "default": 1.0},
        {"name": "moment_of_inertia", "label": "Moment of Inertia, I", "type": "number", "unit": "in^4", "default": 1.0},
        {"name": "factor_of_safety", "label": "Factor of Safety", "type": "number", "default": 2.0},
    ],
    "BOLT": [
        {"name": "nominal_diameter", "label": "Nominal Diameter", "type": "number", "unit": "in", "default": 0.5},
        {"name": "threads_per_inch", "label": "Threads per Inch", "type": "number", "default": 13.0},
        {"name": "proof_strength", "label": "Proof Strength", "type": "number", "unit": "ksi", "default": 85.0},
        {"name": "factor_of_safety", "label": "Factor of Safety", "type": "number", "default": 2.0},
    ],
    "WELD": [
        {"name": "weld_size", "label": "Weld Size", "type": "number", "unit": "in", "default": 0.25},
        {"name": "weld_length", "label": "Weld Length", "type": "number", "unit": "in", "default": 4.0},
        {"name": "applied_load", "label": "Applied Load", "type": "number", "unit": "lbf", "default": 1000.0},
        {"name": "allowable_stress", "label": "Allowable Stress", "type": "number", "unit": "ksi", "default": 18.0},
    ],
    "LUG": [
        {"name": "pin_diameter", "label": "Pin Diameter", "type": "number", "unit": "in", "default": 0.5},
        {"name": "thickness", "label": "Thickness", "type": "number", "unit": "in", "default": 0.5},
        {"name": "edge_distance", "label": "Edge Distance", "type": "number", "unit": "in", "default": 0.75},
        {"name": "load", "label": "Applied Load", "type": "number", "unit": "lbf", "default": 1000.0},
    ],
}

DEFAULT_FIELDS = [
    {"name": "primary_dimension", "label": "Primary Dimension", "type": "number", "default": 1.0},
    {"name": "secondary_dimension", "label": "Secondary Dimension", "type": "number", "default": 1.0},
    {"name": "load", "label": "Applied Load", "type": "number", "default": 100.0},
    {"name": "factor_of_safety", "label": "Factor of Safety", "type": "number", "default": 2.0},
]


def preset_fields_for_category(category: str):
    return CATEGORY_PRESETS.get(category, DEFAULT_FIELDS)
