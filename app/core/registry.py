
from __future__ import annotations

import json
from pathlib import Path
from typing import List, Optional

from app.core.schema_presets import preset_fields_for_category

PLUGIN_ROOT = Path(__file__).resolve().parents[1] / 'plugins'


def _enrich(data: dict) -> dict:
    data.setdefault('ui_mode', 'generic')
    data.setdefault('short_description', f"{data['subcategory']} calculator")
    data.setdefault('tags', [data['top_category'].lower(), data['calc_slug']])
    data.setdefault('generic_fields', preset_fields_for_category(data['top_category']))
    return data


def load_catalog() -> List[dict]:
    tools: List[dict] = []
    for manifest_path in PLUGIN_ROOT.glob('*/*/manifest.json'):
        with open(manifest_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        data['module_path'] = str(manifest_path.parent).replace(str(PLUGIN_ROOT), 'app/plugins')
        tools.append(_enrich(data))
    tools.sort(key=lambda x: (x['top_category'], x['subcategory']))
    return tools


def get_categories(catalog: List[dict]) -> List[str]:
    return sorted({item['top_category'] for item in catalog})


def get_tool(catalog: List[dict], plugin_id: str) -> Optional[dict]:
    for item in catalog:
        if item['plugin_id'] == plugin_id:
            return item
    return None
