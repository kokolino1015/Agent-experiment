# Agent loop from scratch

A minimal tool-calling agent built directly on the Anthropic Python SDK, with no framework. Written to understand what an agent loop is before using one like LangGraph.

## How it works

The model decides, the code executes. Each turn sends the full message history to the model. If the response's `stop_reason` is `tool_use`, the requested tools run locally, their results go back as `tool_result` blocks matched by id, and the loop repeats. Any other stop reason ends the loop. A `MAX_TURNS` guard stops a model that keeps requesting tools.

Tool failures (unknown tool, bad arguments, exceptions) are returned to the model as error results instead of crashing the loop.

## Run

```bash
pip install anthropic python-dotenv
python main.py
```

Needs a `.env` file containing `ANTHROPIC_API_KEY=...` (ignored by git).

## Limits

Toy tools only (`add`, `multiply`). Tool schemas are written by hand next to the functions, so the two can drift apart; frameworks generate schemas from the function itself. History lives in memory, so there is no persistence or resuming.