"""
Standalone inference & isolated `Pass@1` subprocess test helper for
`layer8labs8/OrdoPy-Coder-0.5B`.
"""

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from typing import List, Optional, Tuple

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

DEFAULT_MODEL_ID = "layer8labs8/OrdoPy-Coder-0.5B"
SYSTEM_PROMPT = (
    "You are OrdoPy, an expert Python software engineer and logical problem solver. "
    "Think clearly step-by-step in English and write clean, bug-free Python code."
)

_FORBIDDEN_SCRIPT_RANGES = (
    (0x0400, 0x052F),  # Cyrillic
    (0x0590, 0x05FF),  # Hebrew
    (0x0600, 0x06FF),  # Arabic / Persian
    (0x0900, 0x097F),  # Devanagari
    (0x0E00, 0x0E7F),  # Thai
    (0x1100, 0x11FF),  # Hangul Jamo
    (0x3040, 0x30FF),  # Hiragana & Katakana
    (0x4E00, 0x9FFF),  # CJK Unified Ideographs
    (0xAC00, 0xD7AF),  # Hangul Syllables
)


def contains_forbidden_script(text: str) -> bool:
    for ch in text:
        cp = ord(ch)
        if cp >= 128 and any(lo <= cp <= hi for lo, hi in _FORBIDDEN_SCRIPT_RANGES):
            return True
    return False


def build_non_english_suppress_ids(tokenizer) -> List[int]:
    vocab = tokenizer.get_vocab()
    special_keep = set(getattr(tokenizer, "all_special_ids", []) or [])
    suppress: List[int] = []
    for tok_str, tok_id in vocab.items():
        if tok_id in special_keep or (tok_str.startswith("<|") and tok_str.endswith("|>")):
            continue
        if contains_forbidden_script(tok_str):
            suppress.append(int(tok_id))
    return sorted(suppress)


def extract_python_code(text: str) -> str:
    if not text:
        return ""
    fence_py = re.findall(r"```python\s*\n(.*?)```", text, flags=re.DOTALL | re.IGNORECASE)
    if fence_py:
        return max(fence_py, key=len).strip()
    fence_any = re.findall(r"```\s*\n(.*?)```", text, flags=re.DOTALL)
    if fence_any:
        return max(fence_any, key=len).strip()
    open_py = re.search(r"```(?:python)?\s*\n(.*)", text, flags=re.DOTALL | re.IGNORECASE)
    if open_py:
        return open_py.group(1).strip()
    return text.strip()


def execute_python_test(
    candidate_code: str,
    test_code: str,
    entry_point: str = "",
    timeout_sec: float = 3.0,
) -> Tuple[bool, str]:
    parts = [candidate_code.rstrip(), test_code.strip()]
    if entry_point and "def check(" in test_code and f"check({entry_point})" not in test_code:
        parts.append(f"check({entry_point})")
    program = "\n\n".join(p for p in parts if p) + "\n"
    try:
        proc = subprocess.run(
            [sys.executable, "-I", "-c", program],
            cwd=tempfile.gettempdir(),
            capture_output=True,
            text=True,
            timeout=timeout_sec,
        )
        return (proc.returncode == 0, "pass" if proc.returncode == 0 else "fail")
    except subprocess.TimeoutExpired:
        return False, "timeout"
    except Exception:
        return False, "error"


def generate_python_solution(
    user_prompt: str,
    model_id: str = DEFAULT_MODEL_ID,
    max_new_tokens: int = 256,
    device: Optional[str] = None,
) -> str:
    target_device = device or ("cuda" if torch.cuda.is_available() else "cpu")
    dtype = torch.float16 if target_device == "cuda" else torch.float32
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=dtype).to(target_device)
    model.eval()

    suppress_ids = build_non_english_suppress_ids(tokenizer)
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]
    prompt_text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    enc = tokenizer([prompt_text], return_tensors="pt").to(target_device)
    gen_kwargs = {
        "max_new_tokens": max_new_tokens,
        "do_sample": False,
        "pad_token_id": tokenizer.pad_token_id or tokenizer.eos_token_id,
        "eos_token_id": tokenizer.eos_token_id,
    }
    if suppress_ids:
        gen_kwargs["suppress_tokens"] = suppress_ids
    with torch.no_grad():
        out_ids = model.generate(**enc, **gen_kwargs)
    completion = tokenizer.decode(out_ids[0][enc["input_ids"].shape[1]:], skip_special_tokens=True)
    return extract_python_code(completion)
