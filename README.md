# OrdoPy-Coder-0.5B (`English + Logic + Python`)

[![HuggingFace Model](https://img.shields.io/badge/HuggingFace-layer8labs8%2FOrdoPy--Coder--0.5B-orange.svg)](https://huggingface.co/layer8labs8/OrdoPy-Coder-0.5B)
[![Base Model](https://img.shields.io/badge/Base-Qwen%2FQwen2.5--Coder--0.5B--Instruct-blue.svg)](https://huggingface.co/Qwen/Qwen2.5-Coder-0.5B-Instruct)
[![HumanEval Pass@1](https://img.shields.io/badge/HumanEval%20Pass%401-40.85%25-brightgreen.svg)](#official-execution-benchmarks-pass1--421-tasks)
[![MBPP Pass@1](https://img.shields.io/badge/MBPP%20Pass%401-46.30%25-brightgreen.svg)](#official-execution-benchmarks-pass1--421-tasks)
[![License: MIT](https://img.shields.io/badge/License-MIT-black.svg)](LICENSE)

**OrdoPy-Coder-0.5B** is a compact 0.5B specialist coding and logical reasoning model tuned from `Qwen/Qwen2.5-Coder-0.5B-Instruct` for **Python programming**, **English instruction following**, and **step-by-step problem solving**.

Model weights are hosted on HuggingFace Hub: [`layer8labs8/OrdoPy-Coder-0.5B`](https://huggingface.co/layer8labs8/OrdoPy-Coder-0.5B).

---

## Official Execution Benchmarks (`Pass@1` — 421 Tasks)

Evaluated with greedy decoding inside isolated `3.0s`-timeout `sys.executable -I` subprocesses on the full official test suites (`openai/openai_humaneval` `164` tasks + `google-research-datasets/mbpp` `sanitized` `257` test tasks):

| Benchmark Suite | Baseline (`Qwen2.5-Coder-0.5B-Instruct`) | `OrdoPy-Coder-0.5B` | Gain |
| :--- | :---: | :---: | :---: |
| **HumanEval (`164` tasks)** | `9.76%` (`16/164`) | **`40.85%` (`67/164`)** | **`+31.09%` (`4.19x`)** |
| **MBPP Sanitized Test (`257` tasks)** | `36.58%` (`94/257`) | **`46.30%` (`119/257`)** | **`+9.72%` (`+25` tasks)** |
| **Combined (`421` tasks)** | `26.13%` (`110/421`) | **`44.18%` (`186/421`)** | **`+18.05%` (`+76` tasks)** |

### Official EvalPlus Suite (`evalplus` Greedy `Pass@1`)

| Benchmark Suite | `OrdoPy-Coder-0.5B` `Pass@1` | Passed Tasks |
| :--- | :---: | :---: |
| **HumanEval (`base`)** | **`48.8%`** (`0.4878`) | `80 / 164` |
| **HumanEval+ (`base + extra tests`)** | **`46.3%`** (`0.4634`) | `76 / 164` |
| **MBPP (`base`)** | **`48.4%`** (`0.4841`) | `183 / 378` |
| **MBPP+ (`base + extra tests`)** | **`42.1%`** (`0.4206`) | `159 / 378` |

---

## Held-Out Domain Evaluation

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
│   └── eval_benchmarks.json         # Official 421-task Pass@1 and held-out domain evaluation metrics
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
