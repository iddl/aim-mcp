# aim-mcp

MCP server for [Aim](https://github.com/aimhubio/aim) experiment tracking. Exposes runs, params, and metric data to LLMs.

I use this to ask the following questions

```
> Analyze the latest aim metrics from the latest run and tell me how you think the changes are working out.

```

## Usage

```bash
python aim_mcp.py --repo /path/to/aim/repo
```

Point your MCP client at the server, then ask things like:
