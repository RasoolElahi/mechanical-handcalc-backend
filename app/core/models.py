
from pydantic import BaseModel, Field
from typing import Any, List, Optional


class FieldInfo(BaseModel):
    name: str
    label: str
    type: str = 'number'
    unit: str | None = None
    default: Any = None
    min: float | None = None
    max: float | None = None
    options: List[str] | None = None
    help: str | None = None


class ToolInfo(BaseModel):
    plugin_id: str
    top_category: str
    subcategory: str
    category_slug: str
    calc_slug: str
    module_path: str
    ui_mode: str = 'generic'
    short_description: str | None = None
    tags: List[str] = Field(default_factory=list)
    generic_fields: List[FieldInfo] = Field(default_factory=list)


class CatalogResponse(BaseModel):
    total_tools: int
    categories: List[str]
    tools: List[ToolInfo]


class SolveRequest(BaseModel):
    user_name: str = ''
    inputs: dict = Field(default_factory=dict)


class SolveResponse(BaseModel):
    plugin_id: str
    user_name: str
    status: str
    message: str
    result: dict = Field(default_factory=dict)
