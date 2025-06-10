import asyncio
import json
from fastmcp import FastMCP
import httpx

OLLAMA_HOST = "http://localhost:11434"
DEFAULT_MODEL = "llama3"

server = FastMCP(name="llm-devbox")

@server.tool("ping")
async def ping() -> dict:
    """Simple ping command for health checks."""
    return {"status": "ok", "message": "pong"}

@server.tool("run-inference")
async def run_inference(prompt: str, model: str | None = None) -> dict:
    """Run inference using the locally running Ollama server."""
    if not prompt:
        return {"status": "error", "error": "prompt is required"}

    model_name = model or DEFAULT_MODEL
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{OLLAMA_HOST}/api/generate",
                json={"model": model_name, "prompt": prompt},
            )
            resp.raise_for_status()
            data = resp.json()
        return {"status": "ok", "response": data}
    except Exception as exc:
        return {"status": "error", "error": str(exc)}

@server.tool("list-models")
async def list_models() -> dict:
    """Return the list of available models from Ollama."""
    cmd = ["ollama", "list", "--json"]
    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        if proc.returncode != 0:
            err = stderr.decode().strip() or f"return code {proc.returncode}"
            raise RuntimeError(err)
        models = []
        for line in stdout.decode().splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                name = obj.get("name")
                if name:
                    models.append(name)
            except json.JSONDecodeError:
                continue
        return {"status": "ok", "models": models}
    except Exception as exc:
        return {"status": "error", "error": str(exc)}

def main() -> None:
    asyncio.run(server.run_stdio_async())

if __name__ == "__main__":
    main()
