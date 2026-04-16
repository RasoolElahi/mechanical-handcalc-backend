"""Active backend solver for Column _ Euler_Johnson_AISC360_SSRC."""
from __future__ import annotations
import math

PLUGIN_ID = "buckling__column_euler_johnson_aisc360_ssrc"
TOP_CATEGORY = "BUCKLING"
SUBCATEGORY = "Column _ Euler_Johnson_AISC360_SSRC"

def _to_float(v, default=0.0):
    try:
        return float(v)
    except Exception:
        return default

def get_end_condition_factors(end_condition: str):
    factors = {"Fixed-Free": (2.0, 2.1), "Pinned-Pinned": (1.0, 1.0), "Fixed-Pin": (0.7, 0.8), "Fixed-Fixed": (0.5, 0.65)}
    return factors.get(end_condition, (1.0, 1.0))

def euler_function(lmbda: float) -> float:
    return 1.0 if lmbda <= 1.0 else lmbda**-2

def johnson_function(lmbda: float) -> float:
    if lmbda <= math.sqrt(2.0):
        return 1.0 - (lmbda**2) / 4.0
    return lmbda**-2

def aisc_360_function(lmbda: float) -> float:
    if lmbda < math.sqrt(2.25):
        return 0.658 ** (lmbda**2)
    return 0.877 * lmbda**-2

def ssrc_function(lmbda: float, curve: str) -> float:
    if curve == "Curve # 1":
        if 0 <= lmbda < 0.15: return 1.0
        if 0.15 <= lmbda < 1.2: return 0.990 + 0.112 * lmbda - 0.367 * lmbda**2
        if 1.2 <= lmbda < 1.8: return 0.051 + 0.801 * lmbda**-2
        if 1.8 <= lmbda < 2.8: return 0.008 + 0.942 * lmbda**-2
        return lmbda**-2
    if curve == "Curve # 2":
        if 0 <= lmbda < 0.15: return 1.0
        if 0.15 <= lmbda < 1.0: return 1.035 - 0.202 * lmbda - 0.222 * lmbda**2
        if 1.0 <= lmbda < 2.0: return -0.111 + 0.636 * lmbda**-1 + 0.087 * lmbda**-2
        if 2.0 <= lmbda < 3.6: return 0.009 + 0.877 * lmbda**-2
        return lmbda**-2
    if curve == "Curve # 3":
        if 0 <= lmbda < 0.15: return 1.0
        if 0.15 <= lmbda < 0.8: return 1.093 - 0.622 * lmbda
        if 0.8 <= lmbda < 2.2: return -0.128 + 0.707 * lmbda**-1 - 0.102 * lmbda**-2
        if 2.2 <= lmbda < 5.0: return 0.008 + 0.792 * lmbda**-2
        return lmbda**-2
    return lmbda**-2

def compute_geometry(inputs):
    k_theory, k_aisc = get_end_condition_factors(inputs.get("end_condition", "Fixed-Fixed"))
    cross_section = inputs.get("cross_section", "Circular")
    if cross_section == "Circular":
        inner_diameter = _to_float(inputs.get("inner_diameter", 0.0))
        outer_diameter = _to_float(inputs.get("outer_diameter", 0.63))
        area = math.pi * (outer_diameter**2 - inner_diameter**2) / 4.0
        inertia = math.pi * (outer_diameter**4 - inner_diameter**4) / 64.0
    elif cross_section == "Rectangular":
        width = _to_float(inputs.get("width", 0.63)); height = _to_float(inputs.get("height", 0.63))
        area = width * height
        inertia = min(width * height**3 / 12.0, height * width**3 / 12.0)
    else:
        area = _to_float(inputs.get("area", 0.3117)); inertia = _to_float(inputs.get("inertia", 0.0077))
    L = _to_float(inputs.get("L", 9.0))
    if area <= 0 or inertia <= 0:
        raise ValueError("Area and inertia must be greater than zero.")
    le = k_theory * L; le_aisc = k_aisc * L; r = math.sqrt(inertia / area)
    return area, inertia, le, le_aisc, r

def solve(user_name: str, inputs: dict) -> dict:
    try:
        sigma_y = _to_float(inputs.get("sigma_y", 30.0)); E = _to_float(inputs.get("E", 28500.0)); fs = _to_float(inputs.get("fs", 6.0)); load = _to_float(inputs.get("load", 1033.0))
        method = inputs.get("method", "Euler"); curve = inputs.get("curve", "Curve # 2")
        A, I, Le, Le_AISC, r = compute_geometry(inputs)
        lam = (1.0 / math.pi) * math.sqrt(sigma_y / E) * (Le / r)
        lam_aisc = (1.0 / math.pi) * math.sqrt(sigma_y / E) * (Le_AISC / r)
        sigma_euler = sigma_y * euler_function(lam)
        sigma_johnson = sigma_y * max(johnson_function(lam), 0.0)
        sigma_aisc = sigma_y * aisc_360_function(lam_aisc)
        sigma_ssrc = sigma_y * ssrc_function(lam, curve)
        pcr_euler = sigma_euler * A * 1000.0; pcr_johnson = sigma_johnson * A * 1000.0; pcr_aisc = sigma_aisc * A * 1000.0; pcr_ssrc = sigma_ssrc * A * 1000.0
        mos = {"Euler": (pcr_euler / (fs * load)) - 1.0, "Johnson": (pcr_johnson / (fs * load)) - 1.0, "AISC_360": (pcr_aisc / (fs * load)) - 1.0, "SSRC": (pcr_ssrc / (fs * load)) - 1.0}
        selected = mos.get(method, mos["Euler"])
        return {
            "plugin_id": PLUGIN_ID,
            "user_name": user_name,
            "status": "ok",
            "message": f"Buckling calculation completed. Euler={mos['Euler']:.3f}, Johnson={mos['Johnson']:.3f}, AISC360={mos['AISC_360']:.3f}, SSRC={mos['SSRC']:.3f}, selected={selected:.3f}.",
        }
    except Exception as e:
        return {
            "plugin_id": PLUGIN_ID,
            "user_name": user_name,
            "status": "error",
            "message": f"Buckling calculation failed: {e}",
        }
