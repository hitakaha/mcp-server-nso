# MCP server for NSO
- Python and uv are required prior to the installation.
- runcli package is required, download from following and re-compile if necessary.
https://github.com/hitakaha/runcli


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

Then, copy server.py to the directory.

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
