MCP server for NSO

# How to set up on Windows

Python and uv are required prior to the installation.

## 1. Install Claude
Install Claude from following.

https://claude.ai/download

## 2. Setup python
```
uv init nso
cd nso
uv venv
.venv\Scripts\activate
uv add mcs[cli] httpx
```

Then, copy server.py in this repository.

## 3. Add MCP to Claude
Add following to Claude.

```json
{
  "mcpServers": {
    "nso": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\\Users\\username\\mcp\\nso",
        "run",
        "server.py"
      ]
    }
  }
}
```
