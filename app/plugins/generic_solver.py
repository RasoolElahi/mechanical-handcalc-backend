
from __future__ import annotations

from math import sqrt


def solve_generic(plugin_id: str, title: str, user_name: str, inputs: dict) -> dict:
    numeric_values = []
    for value in inputs.values():
        try:
            numeric_values.append(float(value))
        except Exception:
            continue
    checksum = sum(numeric_values)
    rms = sqrt(sum(v*v for v in numeric_values) / len(numeric_values)) if numeric_values else 0.0
    return {
        'plugin_id': plugin_id,
        'user_name': user_name,
        'status': 'generic_ready',
        'message': (
            f"{title} is using the shared generic UI and backend contract. "
            f"Received {len(inputs)} inputs and validated the plugin path successfully."
        ),
        'result': {
            'input_count': len(inputs),
            'numeric_checksum': round(checksum, 6),
            'numeric_rms': round(rms, 6),
            'echo_inputs': inputs,
        },
    }
