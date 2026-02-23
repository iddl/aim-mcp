import click
from aim import Repo
from fastmcp import FastMCP

mcp = FastMCP("Aim")
repo = None


@mcp.tool()
def list_runs(tag: str = None) -> str:
    """List all runs in the Aim repository, optionally filtered by tag."""
    res = []
    for r in repo.iter_runs():
        try:
            tags = [getattr(t, "name", str(t)) for t in r.tags]
            if tag and tag not in tags:
                continue
            res.append(str({"hash": r.hash, "tags": tags, "experiment": r.experiment, "params": r[...]}))
        except:
            continue
    return "\n".join(res) or "No runs found."


@mcp.tool()
def get_run_details(run_hash: str) -> str:
    """Get details for a specific run including its parameters and available metrics."""
    try:
        r = repo.get_run(run_hash)
        if not r:
            return f"Run {run_hash} not found."
        metrics = [{"name": n, "context": ctx.to_dict()} for n, ctx, _ in r.iter_metrics_info()]
        return str({"hash": r.hash, "metrics": metrics, "params": r[...]})
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def get_metric_data(run_hash: str, metrics: list[dict], n: int = 50) -> str:
    """Get sampled metric data for a run. metrics is a list of {"name": str, "context": dict | None}."""
    # metrics: list of {"name": str, "context": dict | None}, e.g. [{"name": "loss"}, {"name": "learning_rate", "context": {"group": 1}}]
    try:
        r = repo.get_run(run_hash)
        if not r:
            return f"Run {run_hash} not found."

        all_metrics = [(name, ctx) for name, ctx, _ in r.iter_metrics_info()]
        results = []
        for req in metrics:
            metric_name = req["name"]
            context = req.get("context")
            matches = [
                (name, ctx) for name, ctx in all_metrics
                if name == metric_name and (context is None or ctx.to_dict() == context)
            ]
            if not matches:
                results.append({"metric": metric_name, "context": context, "error": "not found"})
                continue
            for name, ctx in matches:
                m = r.get_metric(name, ctx)
                points = [{"step": step, "value": round(val, 6)} for step, (val, _, _) in m.data.sample(n).items()]
                points.sort(key=lambda p: p["step"])
                results.append({"metric": name, "context": ctx.to_dict(), "num_points": len(points), "data": points})

        return str(results) if len(results) > 1 else str(results[0])
    except Exception as e:
        return f"Error: {e}"


@click.command()
@click.option("--port", default=8000, help="Port to run SSE server on")
@click.option("--transport", default="stdio", type=click.Choice(["stdio", "sse"]))
@click.option("--repo", "repo_path", default=".", help="Path to the Aim repo (.aim directory)")
def main(port, transport, repo_path):
    global repo
    repo = Repo(repo_path)
    if transport == "stdio":
        mcp.run(transport="stdio")
    else:
        mcp.run(transport="sse", port=port)


if __name__ == "__main__":
    main()
