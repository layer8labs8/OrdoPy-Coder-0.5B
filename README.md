# OrdoPy-Coder-0.5B (`English + Logic + Python`)

[![HuggingFace Model](https://img.shields.io/badge/HuggingFace-layer8labs8%2FOrdoPy--Coder--0.5B-orange.svg)](https://huggingface.co/layer8labs8/OrdoPy-Coder-0.5B)
[![Base Model](https://img.shields.io/badge/Base-Qwen%2FQwen2.5--Coder--0.5B--Instruct-blue.svg)](https://huggingface.co/Qwen/Qwen2.5-Coder-0.5B-Instruct)
[![License: MIT](https://img.shields.io/badge/License-MIT-black.svg)](LICENSE)

**OrdoPy-Coder-0.5B v2** is `Qwen/Qwen2.5-Coder-0.5B-Instruct` fine-tuned with rejection sampling: the base model's own solutions to 2,000 KodCode problems were run against unit tests, passing ones were kept, and a LoRA adapter trained on them was merged into the weights. It is about on par with the base model and clearly better than v1 (kept under the `v1` tag on Hugging Face).

Model weights are hosted on HuggingFace Hub: [`layer8labs8/OrdoPy-Coder-0.5B`](https://huggingface.co/layer8labs8/OrdoPy-Coder-0.5B).

---

## Benchmarks (EvalPlus, greedy `pass@1`)

Base and v2 were scored by the official [EvalPlus](https://github.com/evalplus/evalplus) harness in the **same run** (Kaggle 2x T4, `float16`):

| Benchmark | Base, official¹ | Base, same run | **v2 (this model)** | v1 (previous upload) |
| :--- | :---: | :---: | :---: | :---: |
| HumanEval | `61.6` | `57.9` | **`61.0`** | `48.8` |
| HumanEval+ | `57.3` | `53.7` | **`55.5`** | `46.3` |
| MBPP | `52.4` | `52.1` | `51.1` | `48.4` |
| MBPP+ | `43.7` | `44.2` | `41.0` | `42.1` |
| **Average** | — | `52.0` | **`52.2`** | `46.4` |

¹ [Qwen2.5-Coder Technical Report](https://arxiv.org/abs/2409.12186), Table 16 (Qwen's own evaluation setup).

**Honest summary:** v2 is clearly better than v1 (+5.8 points on average) and **about on par with the base model** (better on HumanEval / HumanEval+, worse on MBPP / MBPP+; single seed, differences of this size are close to run-to-run noise). It does not beat the base model overall.

> **About v1.** The first upload is kept under the `v1` tag of this repository (`AutoModelForCausalLM.from_pretrained("layer8labs8/OrdoPy-Coder-0.5B", revision="v1")`). It was a supervised fine-tune that scores below the base model on all four benchmarks. Its card claimed HumanEval `9.76% -> 40.85%`; that comparison was a measurement error (a 224-token generation cap truncated the base model's answers, and the checkpoint was selected on test slices). `eval_benchmarks.json` in this repository is v1 training telemetry. Full v2 report and code: [OrdoTrain](https://github.com/layer8labs8/OrdoTrain) (`results/ordopy_rft_lora_report.json`).

---

## v1 Held-Out Domain Evaluation (token-level loss)

v1 telemetry: token-level loss on held-out splits improved slightly, but this did not translate into better pass@1.


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
