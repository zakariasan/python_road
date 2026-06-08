import json
import sys
from pathlib import Path
from .funcDef import FuncDef, Prompt

def load_file(path: str) -> list[dict]:
    """loading files from inpput 

    Args:
        path: where file lives

    Returns:
        list of what file has according json structure
    """

    local_path = Path(path)

    if not local_path.exists():
        print(f'ERROR: file not found: {path}')
        sys.exit(1)

    try:
        info = json.loads(local_path.read_text(encoding='utf-8'))
    except json.JSONDecodeError as e:
        print(f'ERROR: invalid json file')
        sys.exit(1)

    if not isinstance(info, list):
        print(f'ERROR: expected a list in the ')
        sys.exit(1)

    return info


def load_func(path: str) -> list[FuncDef]:
    """ Load and check the func def
    
    Args:
        path: where data lives

    Returns:
        list of FunctionDef
    """

    data = load_file(path)
    out = []

    for i, item in enumerate(data):
        try:
            out.append(FuncDef.model_validate(item))
        except Exception as e:
            print(f'ERROR: function at index {i} is invalid: {e}')
            sys.exit(1)
    return out

def load_prompt(path: str) -> list[Prompt]:
    """ Load and check the prompt def
    
    Args:
        path: where data lives

    Returns:
        list of prompts 
    """

    data = load_file(path)
    out = []

    for i, item in enumerate(data):
        try:
            out.append(Prompt.model_validate(item))
        except Exception as e:
            print(f'ERROR: Prompt at index {i} is invalid: {e}')
            sys.exit(1)
    return out


def build_prompt(prompt: str, functions: list[FuncDef]) -> str:
    """merge prompt with functions calling so the llm can predicted 

    Args:
        prompt: what humans says
        functions: what we can help with

    Returns:
        a string of data
    """
    lines = ["Available functions:"]
    for fn in functions:
        params = ", ".join(f"{k}: {v.type}" for k, v in fn.parameters.items())
        lines.append(f"- {fn.name}({params})")
    lines.append(f"\nUser request: {prompt}\n\nOutput:")
    return "\n".join(lines)
