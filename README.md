# Math LLM

This is a prototype project for grounding mathematical reasoning for large language models, using software proof assistants.

This repo is _highly_ experimental, and anything might break at any time or not work for you.

Contributions are welcome.

## Installation

You will need the `coqtop` command line application. This is a CLI for interacting with the [Coq](https://coq.inria.fr/download) proof assistant software. I used the default installation path and it worked out of the box following the instructions in the included README.

You will need an [OpenAI API Key](https://platform.openai.com/account/api-keys) set in the OPENAI_API_KEY environment variable.

Then run `pip install -r requirements.txt`

## Run

`python main.py`

## Roadmap

- [x] Interactively use Coq from Python
- [x] Use LLM to generate proofs in a readable format
- [x] Execute generated Coq
- [x] Use LLM to evaluate proofs for logical consistency
- [ ] Store proof results in memory
- [ ] Generate new conjectures
- [ ] Break down proofs recursively into sub-goals
- [ ] ...
