from llm_sdk import Small_LLM_Model
import json
import numpy as np
import argparse
from .funcDef import FuncDef
from .load_file import load_func, load_prompt, build_prompt 
from .constrainDecoder import ConstrainedDecoder


def building(
        model: Small_LLM_Model,
        ids: list[int],
        functions: list[FuncDef],
        max_tokens: int = 100
        ) -> str:
    """Run the token-by tokengeneration loop

    Args:
        model: our Mohmad slm that gonna make it
        functions: our tools
        max_tokens: saftly token

    Returns:
        text
    """
    decoder = ConstrainedDecoder(functions, model.get_path_to_vocab_file())
    
    ids_cpy = ids.copy()
    generated = ''

    for _ in range(max_tokens):
        logits = model.get_logits_from_input_ids(ids_cpy)
        masked = decoder.mask_logits(logits, generated)

        if np.all(masked == float('-inf')):
            print(f'BN: all token masked')
            break

        # constrain decoding here

        next_id = int(np.argmax(masked))
        next_str = decoder.id_to_clean.get(next_id, '')

        ids_cpy.append(next_id)
        generated += next_str

        if generated.endswith("}}"):
            break

    return generated
    
def parser() -> argparse.Namespace:
    """Parse command line command"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
            "--functions_definition", 
            default="data/input/functions_definition.json"
            )
    parser.add_argument(
            "--input", default="data/input/function_calling_tests.json")
    parser.add_argument("--output", default="data/output/function_calls.json")
    return parser.parse_args()


def main():
    args = parser()
    
    
    functions = load_func(args.functions_definition)
    prompts = load_prompt(args.input)

    model = Small_LLM_Model()


    for p in prompts:
        context = build_prompt(p, functions)
        ids = model.encode(context)[0].tolist()
        res = building(model, ids, functions)
        print(f'prompt: {p.prompt}')
        print(f'out: {res}')
        print('+++++++++++++++++++++++++')

if __name__ == "__main__":
    main()
