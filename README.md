# Evaluating Implicit Biases in LLM Reasoning through Logic Grid Puzzles

We introduce PRIME (**P**uzzle **R**easoning for **I**mplicit Biases in **M**odel **E**valuation) a novel evaluation framework that uses [logic grid puzzles](https://en.wikipedia.org/wiki/Logic_puzzle) to systematically probe the influence of social stereotypes on logical reasoning and decision making in LLMs. PRIME includes stereotypical, anti-stereotypical, and generic puzzle variants generated from a shared puzzle structure, allowing for controlled and fine-grained comparisons. Our use of logic puzzles enables automatic generation and verification, as well as variability in complexity and biased settings.

<img width="2619" height="1158" alt="image" src="https://github.com/user-attachments/assets/3529a83e-af42-4771-8d3e-6cfeabdb7c15" />

---
## Installation

```bash
git clone https://github.com/FatimaJahara/PRIME.git
cd PRIME
pip install -e .
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



