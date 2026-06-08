from pydantic import BaseModel
from typing import Dict, Any

class ParamDef(BaseModel):
    type: str

class FuncDef(BaseModel):
    name: str
    description: str
    parameters : Dict[str, ParamDef] = {}
    returns: ParamDef

class Prompt(BaseModel):
    prompt: str

class FunCall(BaseModel):
    prompt: str
    name: str
    params: dict[str, ParamDef] = {}
