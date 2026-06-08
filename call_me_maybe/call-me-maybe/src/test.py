from llm_sdk import Small_LLM_Model
import json
import numpy as np

def main():
    print("=== Loading model... ===")
    model = Small_LLM_Model()
    print("Model loaded!\n")
    
    # ─────────────────────────────────────────
    # STEP 1: encode — text → token ids
    # ─────────────────────────────────────────

    print("=== STEP 1: encode ===")

    prompt = "hello zakaria"
    res = model.encode(prompt)

    print(f"Input : {prompt}")
    print(f'result: {res}')
    print(f'shape : {res.shape}')
    
# ─────────────────────────────────────────
# STEP 2: decode — token ids → text back
# ─────────────────────────────────────────
    ids = res[0].tolist()
    print("as list      :", ids)
    print("token count  :", len(ids))
    print("Hello from call-me-maybe!")
    # ─────────────────────────────────────────
# STEP 3: logits — what does the model predict next?
# ─────────────────────────────────────────
    print("\n=== STEP 3: logits ===")
    logits = model.get_logits_from_input_ids(ids)
    print("logits length (vocab size):", len(logits))
    print("first 5 values            :", logits[:5])

    arr = np.array(logits)
    top5_ids = np.argsort(arr)[-5:][::-1]
    print("\nTop 5 predicted next token IDs:", top5_ids.tolist())
    print("Their scores                  :", arr[top5_ids].tolist())

# ─────────────────────────────────────────
# STEP 4: decode those top 5 tokens
# ─────────────────────────────────────────
    print("\n=== STEP 4: what are those top 5 tokens? ===")
    for token_id in top5_ids:
        token_str = model.decode([int(token_id)])
        print(f"  id {token_id:6} → '{token_str}'")

# ─────────────────────────────────────────
# STEP 5: generate freely — NO constrained decoding
# just let the model predict token by token
# ─────────────────────────────────────────
    print("\n=== STEP 5: free generation (10 tokens) ===")
    current_ids = ids.copy()
    generated = []

    for i in range(10):
        logits = model.get_logits_from_input_ids(current_ids)
        arr = np.array(logits)
        next_id = int(np.argmax(arr))          # pick highest score
        next_str = model.decode([next_id])
        print(f"  step {i+1}: id={next_id}  token='{next_str}'")
        current_ids.append(next_id)
        generated.append(next_id)

    print("\nFull generated text:")
    print(model.decode(generated))

