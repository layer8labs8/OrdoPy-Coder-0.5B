# OrdoPy-Coder-0.5B (`English + Logic + Python`)

[![HuggingFace Model](https://img.shields.io/badge/HuggingFace-layer8labs8%2FOrdoPy--Coder--0.5B-orange.svg)](https://huggingface.co/layer8labs8/OrdoPy-Coder-0.5B)
[![Base Model](https://img.shields.io/badge/Base-Qwen%2FQwen2.5--Coder--0.5B--Instruct-blue.svg)](https://huggingface.co/Qwen/Qwen2.5-Coder-0.5B-Instruct)
[![License: MIT](https://img.shields.io/badge/License-MIT-black.svg)](LICENSE)

**OrdoPy-Coder-0.5B** is a compact 0.5B specialist coding and logical reasoning model tuned from `Qwen/Qwen2.5-Coder-0.5B-Instruct` for **Python programming**, **English instruction following**, and **step-by-step problem solving**.

Model weights are hosted on HuggingFace Hub: [`layer8labs8/OrdoPy-Coder-0.5B`](https://huggingface.co/layer8labs8/OrdoPy-Coder-0.5B).

---

## Benchmarks (EvalPlus, greedy `pass@1`)

Scored with the official [EvalPlus](https://github.com/evalplus/evalplus) harness (`evalplus 0.4.0`), compared with the official numbers for the base model ([Qwen2.5-Coder Technical Report](https://arxiv.org/abs/2409.12186), Table 16):

| Benchmark | `Qwen2.5-Coder-0.5B-Instruct` (official) | `OrdoPy-Coder-0.5B` | Delta |
| :--- | :---: | :---: | :---: |
| **HumanEval** | `61.6%` | `48.8%` (`80 / 164`) | `-12.8` |
| **HumanEval+** | `57.3%` | `46.3%` (`76 / 164`) | `-11.0` |
| **MBPP** | `52.4%` | `48.4%` (`183 / 378`) | `-4.0` |
| **MBPP+** | `43.7%` | `42.1%` (`159 / 378`) | `-1.6` |

> **Correction (November 2026).** An earlier version of this card reported HumanEval rising from `9.76%` to `40.85%` (`4.19x`). That comparison was wrong: the in-house evaluation cut generations at 224 new tokens, which truncated many of the base model's longer answers, and the checkpoint was selected on a slice of the test sets. Measured with EvalPlus, **this fine-tune scores below its base model on all four benchmarks**. If you need the strongest 0.5B coder, use [`Qwen/Qwen2.5-Coder-0.5B-Instruct`](https://huggingface.co/Qwen/Qwen2.5-Coder-0.5B-Instruct) directly. A follow-up experiment (rejection-sampling fine-tune with LoRA on the base model's own test-verified solutions) did not degrade the model but also gave no clear gain (HumanEval `+3.1`, HumanEval+ `+1.8`, MBPP `-1.0`, MBPP+ `-3.2` vs the base measured in the same run); details in the [OrdoTrain repository](https://github.com/layer8labs8/OrdoTrain).

---

## Held-Out Domain Evaluation (token-level loss)

Token-level loss on held-out splits improved slightly, but this did not translate into better pass@1 (see above).


| Domain (Held-Out Split) | Baseline Loss (PPL / Token Acc) | `OrdoPy-Coder-0.5B` Loss (PPL / Token Acc) | Gain |
| :--- | :---: | :---: | :---: |
| **`python_code`** (`MBPP Sanitized Val`) | `1.0226` (`2.78` / `76.44%`) | **`0.9843` (`2.68` / `78.40%`)** | **`+1.96%` Acc** |
| **`logic_math`** (`GSM8K Official Test`) | `1.4752` (`4.37` / `73.21%`) | **`1.4096` (`4.09` / `74.68%`)** | **`+1.47%` Acc** |
| **`english_debug`** (`Alpaca Held-Out`) | `1.6227` (`5.07` / `59.53%`) | **`1.4409` (`4.22` / `61.58%`)** | **`+2.05%` Acc** |

---

## Quickstart Inference & Verification

### Install Dependencies

```bash
pip install torch transformers accelerate
```

### Run Python Generation + Unit-Test Execution

```python
from inference import generate_python_solution, execute_python_test

prompt = "Write a Python function `sum_even(nums: list[int]) -> int` returning the sum of even integers."
code = generate_python_solution(prompt)
print(code)

ok, status = execute_python_test(code, "assert sum_even([1, 2, 3, 4]) == 6")
print("Execution check:", ok, status)
```

---

## Repository Contents

```text
OrdoPy-Coder-0.5B/
├── inference.py                     # HuggingFace loader, non-English token guard & subprocess evaluator
├── configs/
│   ├── config.json
│   ├── generation_config.json
│   ├── tokenizer_config.json
│   └── chat_template.jinja
├── results/
│   └── eval_benchmarks.json         # Raw training-run telemetry (its in-house pass@1 numbers are superseded by EvalPlus above)
├── LICENSE
└── README.md
```

---

## Citation & License

```bibtex
@software{ordopy_coder_2026,
  author       = {{Layer8 Labs}},
  title        = {{OrdoPy-Coder-0.5B: Compact Python, Logic, and English Specialist Model}},
  year         = {2026},
  publisher    = {GitHub},
  url          = {https://github.com/layer8labs8/OrdoPy-Coder-0.5B}
}
```

Released under the [MIT License](LICENSE). Copyright © 2026 **Layer8 Labs**. Model weights: [`layer8labs8/OrdoPy-Coder-0.5B`](https://huggingface.co/layer8labs8/OrdoPy-Coder-0.5B).
