"""Main part constrain decoding"""
"""Constrained decoding — forces valid JSON output."""
import json
import numpy as np
from .funcDef import FuncDef

NEG_INF = float('-inf')
FIXED_START = '{"name": "'
FIXED_MIDDLE = '", "parameters": {'
FIXED_END = '}}'


def _clean(token: str) -> str:
    """BPE token → readable string."""
    return token.replace('Ġ', ' ').replace('Ċ', '\n')


class ConstrainedDecoder:
    """Forces output to match: {"name": "fn_x", "parameters": {"p": v}}"""

    def __init__(
        self,
        functions: list[FuncDef],
        vocab_path: str
    ) -> None:
        self.fn_map: dict[str, FuncDef] = {
            fn.name: fn for fn in functions
        }
        self.fn_names: list[str] = list(self.fn_map.keys())

        with open(vocab_path) as f:
            token_to_id: dict[str, int] = json.load(f)

        self.id_to_clean: dict[int, str] = {
            v: _clean(k) for k, v in token_to_id.items()
        }

    def mask_logits(
        self,
        logits: list[float],
        generated: str
    ) -> np.ndarray:
        """Set invalid token logits to -inf.

        Args:
            logits: raw logits from get_logits_from_input_ids().
            generated: text generated so far after Output:.

        Returns:
            masked logits array.
        """
        masked = np.full(len(logits), NEG_INF, dtype=np.float32)

        for tid, tstr in self.id_to_clean.items():
            if tid < len(logits) and tstr:
                if self._is_valid(generated, tstr):
                    masked[tid] = logits[tid]

        return masked

    def _is_valid(self, generated: str, token: str) -> bool:
        """Check if appending token keeps the output valid."""
        return self._is_valid_prefix(generated + token)

    def _is_valid_prefix(self, candidate: str) -> bool:
        """Check if candidate is a valid prefix of some complete output."""

        # phase 1: fixed start '{"name": "'
        n = min(len(candidate), len(FIXED_START))
        if candidate[:n] != FIXED_START[:n]:
            return False
        if len(candidate) <= len(FIXED_START):
            return True

        after_start = candidate[len(FIXED_START):]

        # phase 2: function name — LLM picks, we constrain to valid names
        q = after_start.find('"')
        if q == -1:
            return any(fn.startswith(after_start) for fn in self.fn_names)

        fn_name = after_start[:q]
        if fn_name not in self.fn_map:
            return False
        fn = self.fn_map[fn_name]

        # phase 3: fixed middle '", "parameters": {'
        after_fn = after_start[len(fn_name):]
        n = min(len(after_fn), len(FIXED_MIDDLE))
        if after_fn[:n] != FIXED_MIDDLE[:n]:
            return False
        if len(after_fn) <= len(FIXED_MIDDLE):
            return True

        # phase 4: parameters
        params_text = after_fn[len(FIXED_MIDDLE):]
        return self._is_valid_params(params_text, list(fn.parameters.items()))

    def _is_valid_params(
        self,
        text: str,
        params: list[tuple]
    ) -> bool:
        """Check if text is a valid prefix of the parameters section."""
        for i, (name, pdef) in enumerate(params):

            # comma separator between params
            if i > 0:
                sep = ', '
                if not text.startswith(sep):
                    return sep.startswith(text)
                text = text[len(sep):]

            # key: "name": value
            key = f'"{name}": '
            if not text.startswith(key):
                return key.startswith(text)
            text = text[len(key):]

            # value — constrained by type
            if pdef.type in ('number', 'integer'):
                j = 0
                while j < len(text) and text[j] in '0123456789.-':
                    j += 1
                if j == 0:
                    return True  # number not started yet
                text = text[j:]
                if not text:
                    return True  # number not finished yet

            elif pdef.type == 'string':
                if not text.startswith('"'):
                    return not text  # waiting for opening quote
                text = text[1:]
                q = text.find('"')
                if q == -1:
                    return True  # string not closed yet
                text = text[q + 1:]

            elif pdef.type == 'boolean':
                for b in ('true', 'false'):
                    if b.startswith(text):
                        return True
                    if text.startswith(b):
                        text = text[len(b):]
                        break
                else:
                    return False

        # all params done — expect '}}'
        return FIXED_END.startswith(text) if text else True
