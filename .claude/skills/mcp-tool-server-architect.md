
---

```yaml
name: "mcp-tool-server-architect"
description: "Blueprints for building a custom MCP server for the Todo App."
---
# Implementation Rules
1. Use the Official Python MCP SDK.
2. Ensure every Task Manager function in `manager.py` has a corresponding `@server.list_tools()` entry.
3. Integrate with the existing GitHub MCP context to ensure tool documentation is automatically updated in the README.
4. Security: Ensure the MCP tools verify JWT tokens just like the FastAPI REST endpoints (Phase II/III Bridge).
