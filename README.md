# MCP server for Aim (Aimhubio/Aimstack)

MCP server for [Aim](https://github.com/aimhubio/aim).
Exposes runs, params, and metric data to LLMs.

I use this to ask the following questions:

- _Analyze the latest Aim metrics from the most recent run and summarize how the changes appear to be working._
- _Compare gradients between runs `6d6c3226...` and `e2ea06cc...`, focusing on AdaLN weight gradients, and explain the key takeaways._
- _Review the latest run `c37d034b...` and interpret the `x`, `y`, and `z` metrics._

## Installation

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

```
python aim_mcp.py --repo /path/to/aim/repo --transport sse --port 8000
```

## Warnings

- **Minimal work went into this**, built over a weekend with Gemini doing most of the coding. However, the codebase is small
- Aim appears to be marginally maintained
- There are no tests
- Best-effort help and support only
