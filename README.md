# LLM Devbox MCP Server

This repository contains a small server built with [FastMCP](https://pypi.org/project/fastmcp/) that exposes a few tools for interacting with a local [Ollama](https://ollama.com/) instance.

## Commands

- `ping` – simple health‑check returning `{"status": "ok", "message": "pong"}`.
- `run-inference` – send a prompt to the configured model on the local Ollama server.
- `list-models` – returns the names of models available via `ollama list`.

All responses include a top‑level `status` field so clients can easily detect success or error conditions.

## Running

Make sure you have Ollama running locally and then start the MCP server:

```bash
python llm_devbox_server.py
```

The server communicates using the MCP protocol over `stdio`.
