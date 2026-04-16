
from fastapi import APIRouter, HTTPException
from pathlib import Path
import csv
from app.core.models import CatalogResponse, SolveRequest, SolveResponse
from app.core.registry import load_catalog, get_categories, get_tool
from app.core.plugin_loader import load_plugin_module
from app.plugins.generic_solver import solve_generic

router = APIRouter()

@router.get('/health')
def health():
    return {'status': 'ok'}

@router.get('/materials')
def materials():
    csv_path = Path(__file__).resolve().parents[1] / 'material_library' / 'materials.csv'
    if not csv_path.exists():
        return {'count': 0, 'materials': []}
    with open(csv_path, 'r', encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    return {'count': len(rows), 'materials': rows}

@router.get('/catalog', response_model=CatalogResponse)
def catalog():
    tools = load_catalog()
    return {
        'total_tools': len(tools),
        'categories': get_categories(tools),
        'tools': tools,
    }

@router.get('/catalog/{plugin_id}')
def catalog_item(plugin_id: str):
    tools = load_catalog()
    item = get_tool(tools, plugin_id)
    if not item:
        raise HTTPException(status_code=404, detail='Calculation not found')
    return item

@router.post('/solve/{plugin_id}', response_model=SolveResponse)
def solve(plugin_id: str, payload: SolveRequest):
    tools = load_catalog()
    item = get_tool(tools, plugin_id)
    if not item:
        raise HTTPException(status_code=404, detail='Calculation not found')

    if item.get('ui_mode') == 'custom':
        try:
            mod = load_plugin_module(item['module_path'])
            if hasattr(mod, 'solve'):
                result = mod.solve(payload.user_name, payload.inputs or {})
                if isinstance(result, dict):
                    result.setdefault('result', {})
                    return result
        except Exception as exc:
            return {
                'plugin_id': plugin_id,
                'user_name': payload.user_name,
                'status': 'error',
                'message': f'Custom solver failed: {exc}',
                'result': {},
            }

    return solve_generic(plugin_id, item['subcategory'], payload.user_name, payload.inputs or {})
