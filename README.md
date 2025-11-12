# [Evaluating Implicit Biases in LLM Reasoning through Logic Grid Puzzles](https://arxiv.org/pdf/2511.06160)

We introduce PRIME (**P**uzzle **R**easoning for **I**mplicit Biases in **M**odel **E**valuation) a novel evaluation framework that uses [logic grid puzzles](https://en.wikipedia.org/wiki/Logic_puzzle) to systematically probe the influence of social stereotypes on logical reasoning and decision making in LLMs. PRIME includes stereotypical, anti-stereotypical, and generic puzzle variants generated from a shared puzzle structure, allowing for controlled and fine-grained comparisons. Our use of logic puzzles enables automatic generation and verification, as well as variability in complexity and biased settings.

<img width="2619" height="1158" alt="image" src="https://github.com/user-attachments/assets/3529a83e-af42-4771-8d3e-6cfeabdb7c15" />

---
## Installation

```bash
git clone https://github.com/FatimaJahara/PRIME.git
cd PRIME
```
### Install dependencies
```bash
pip install -r requirements.txt
```

## Package Structure

```
PRIME/                                # Framework for puzzle generation and evaluation
├── clues/                            # Modules for clue creation and conversion
├── data/                             # Datasets and category mappings
│   ├── categories and items/         # Contains gender bias probing data, name mappings for gender probing, and neutral category dataset
│   └── puzzle dataset/               # Stores PRIME dataset
├── evaluation/                       # Puzzle evaluation and metrics
├── output/                           # Stores generated puzzles as JSON
├── puzzle/                           # Create puzzle structure
├── solver/                           # Logic solver for different clue types
└── utils/                            # Normalization functions
```

## Generate PRIME Puzzles

```bash
python generate_puzzles.py --rows <num_rows> --cols <num_cols> [--out <output_dir>] [--start_id <id>] [--batch <num_puzzles>]
```
**Note:** If the python command doesn’t work on your system, use python3 instead.
  ```
--rows        Number of puzzle rows (must be even)
--cols        Number of puzzle columns
--out         (optional) Output directory for saving puzzles (default: output/)
--start_id    (optional) Starting ID for puzzle naming (default: 1)
--batch       (optional) Number of puzzles to generate (default: 1)
  ```

### Example Generation
**Generate a 4×3 puzzle (rows must be even)**
```bash
python generate_puzzles.py --rows 4 --cols 3
```
**Generate a 4×3 puzzle in a custom directory**
```bash
python generate_puzzles.py --rows 4 --cols 3 --out puzzles/
```
**Generate a single 4×3 puzzle with a custom starting ID**
```bash
python3 generate_puzzles.py --rows 4 --cols 3 --start_id 10
```
**Generate a batch of 10 puzzles (4×3 each)**
```bash
python generate_puzzles.py --rows 4 --cols 3 --batch 10
```
**Generate 50 puzzles starting from ID 101 and save to a custom directory**
```bash
python3 generate_puzzles.py --rows 4 --cols 3 --batch 50 --start_id 101 --out data/puzzles/
```

### Output JSON Format
```
{
  "id": ...,
  "probing_type": "gender_probing",
  "rows": ...,
  "columns": ...,
  "bias_probing_category": "...",
  "bias_probing_names_male": [...],
  "bias_probing_names_female": [...],
  "bias_probing_values_male": [...],
  "bias_probing_values_female": [...],
  "versions": {
    "generic": {
      "solved": true,
      "puzzle_table": {...},
      "clues": {
        "all_clues": [...],
        "solution_clues": [...],
        "solved_constraints": [...]
      }
    },
    "stereotypical": { "...": "..." },
    "anti_stereotypical": { "...": "..." }
  }
}
```
## Generate Natural Language Clues
This step converts logical clues into natural language clues using an LLM through the Together API.
### Set Your Together API Key
**Option 1 — In Colab or Python**
```bash
import os
os.environ["TOGETHER_API_KEY"] = "your_together_api_key_here"
```
**Option 2 — In Terminal (Mac/Linux)**
```bash
export TOGETHER_API_KEY="tg-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```
**Option 3 — In PowerShell (Windows)**
```bash
setx TOGETHER_API_KEY "tg-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

**Run Conversion via CLI**
```bash
python clues/convert_to_natural_language.py \
  --src <source-dir> \
  --dest <output-dir> \
  --api_key $TOGETHER_API_KEY
```

**Note:** Although the current implementation uses  Llama-3.3-70B-Instruct-Turbo via Together AI, you can easily swap this out for any other LLM API (e.g., OpenAI, Anthropic, Mistral, Groq, or local models). Simply modify the [convert_to_natural_language.py](https://github.com/FatimaJahara/PRIME/blob/main/clues/convert_to_natural_language.py) to call your preferred API or local inference endpoint.


## Citation
We kindly request that you cite our paper if you use, build upon, or reference this codebase or dataset in your research.
```
@misc{jahara2025evaluatingimplicitbiasesllm,
      title={Evaluating Implicit Biases in LLM Reasoning through Logic Grid Puzzles}, 
      author={Fatima Jahara and Mark Dredze and Sharon Levy},
      year={2025},
      eprint={2511.06160},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2511.06160}, 
}
```
