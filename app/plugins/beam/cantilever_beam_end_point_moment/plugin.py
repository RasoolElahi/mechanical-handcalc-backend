"""Active backend solver for Cantilever beam - end point moment."""
from __future__ import annotations
import math

PLUGIN_ID = "beam__cantilever_beam_end_point_moment"
TOP_CATEGORY = "BEAM"
SUBCATEGORY = "Cantilever beam - end point moment"

def _to_float(v, default=0.0):
    try:
        return float(v)
    except Exception:
        return default

def _calc_section_properties(inputs: dict):
    section_type = inputs.get("section_type", "Circular Tube")
    rect_axis = inputs.get("rect_axis", "Weak Axis")
    d_in = _to_float(inputs.get("d_in", 0.0))
    d_out = _to_float(inputs.get("d_out", 1.0))
    rect_len = _to_float(inputs.get("rect_len", 1.0))
    rect_wid = _to_float(inputs.get("rect_wid", 1.0))
    arb_area = _to_float(inputs.get("arb_area", 1.0))
    arb_I = _to_float(inputs.get("arb_I", 1.0))
    arb_c = _to_float(inputs.get("arb_c", 0.5))

    if section_type == "Circular Tube":
        area = math.pi / 4.0 * (d_out**2 - d_in**2)
        I = math.pi / 64.0 * (d_out**4 - d_in**4)
        c = d_out / 2.0
    elif section_type == "Rectangle":
        if rect_axis == "Weak Axis":
            t_val = min(rect_len, rect_wid)
            b_val = max(rect_len, rect_wid)
        else:
            t_val = max(rect_len, rect_wid)
            b_val = min(rect_len, rect_wid)
        area = b_val * t_val
        I = b_val * (t_val**3) / 12.0
        c = t_val / 2.0
    else:
        area = arb_area
        I = arb_I
        c = arb_c
    Z = I / c if c > 0 else 0.0
    return area, I, c, Z

def solve(user_name: str, inputs: dict) -> dict:
    sigma_y = _to_float(inputs.get("sigma_y", 30.0))
    sigma_u = _to_float(inputs.get("sigma_u", 58.0))
    E = _to_float(inputs.get("E", 28500.0))
    fs_y = _to_float(inputs.get("fs_y", 2.0))
    fs_u = _to_float(inputs.get("fs_u", 3.0))
    beam_length = _to_float(inputs.get("beam_length", 10.0))
    M = _to_float(inputs.get("M", 40.0))
    area, I, c, Z = _calc_section_properties(inputs)
    if I <= 0 or c <= 0 or Z <= 0:
        return {
            "plugin_id": PLUGIN_ID,
            "user_name": user_name,
            "status": "error",
            "message": "Invalid section properties. Please check your geometry inputs.",
        }
    sigma_root_psi = M * c / I
    sigma_root_ksi = sigma_root_psi / 1000.0
    ms_y = sigma_y / (fs_y * sigma_root_ksi) - 1.0 if sigma_root_ksi > 0 else float("inf")
    ms_u = sigma_u / (fs_u * sigma_root_ksi) - 1.0 if sigma_root_ksi > 0 else float("inf")
    delta_B = M * (beam_length**2) / (2.0 * E * 1000.0 * I) if E > 0 else 0.0
    return {
        "plugin_id": PLUGIN_ID,
        "user_name": user_name,
        "status": "ok",
        "message": f"Beam calculation completed. Stress={sigma_root_psi:.3f} psi, MSy={ms_y:.4f}, MSu={ms_u:.4f}, deflection={delta_B:.6f} in.",
    }
