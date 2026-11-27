# VS2026Handbook_chapter25

A Python example repository for Chapter 25 of the Visual Studio 2026 handbook.

## Contents

- `agent.py` — interactive agent example that sends prompts to a local Ollama server and safely executes date or calculator tool requests.
- `agent_tools.py` — standalone examples for safely evaluating basic arithmetic expressions.
- `VS2026Handbook_chapter25.py` — primary Python source file.
- `VS2026Handbook_chapter25.pyproj` — Visual Studio Python project configuration.
- `VS2026Handbook_chapter25.slnx` — Visual Studio solution file.

## Requirements

- Python 3
- Ollama running locally for `agent.py`
- A model available in Ollama (defaults to `qwen3.5:4b`)

## Usage

Run the standalone tool examples:

```bash
python agent_tools.py
```

Run the interactive agent:

```bash
python agent.py
```

Set a different Ollama model with the `OLLAMA_MODEL` environment variable:

```bash
OLLAMA_MODEL=qwen3.5:4b python agent.py
```
