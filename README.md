# AI Agent Creator

A local, no-API-key AI agent creator built around an offline LLM through Ollama.

## Features
- Create custom agents with role, goal, and instructions
- Build a system prompt automatically
- Store agent configuration as JSON
- Run agents locally without an API key
- Agent memory support
- Extensible tool registry

## Requirements
- Python 3.10+
- Ollama installed locally
- A local model available, such as `llama3.1`

## Install

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Start Ollama

```bash
ollama serve
ollama pull llama3.1
```

## Create an agent

```bash
python app.py create \
  --name "Research Copilot" \
  --role "A research assistant" \
  --goal "Help users understand topics clearly and accurately" \
  --instruction "Be concise" \
  --instruction "Use memory when useful" \
  --instruction "Never fabricate facts" \
  --tool "memory" \
  --tool "search" \
  --model llama3.1
```

This will create a JSON file in `agents/`.

## Run an agent

```bash
python app.py run \
  --agent agents/research_copilot.json \
  --prompt "Explain the difference between a local agent and a cloud AI agent."
```

## Notes
- No API key is required.
- This project expects a local model provider such as Ollama.
- You can expand the app by adding more tools and workflows.

## Project structure

```text
ai-agent-creator-local/
├── app.py
├── agent_core.py
├── local_model.py
├── requirements.txt
├── README.md
├── .gitignore
├── agents/
│   └── .gitkeep
├── memory/
│   └── memory.json
└── .venv/
```
