# LLM Agent Tool Execution Template

A Python starting point for validating a model-proposed tool call before execution. The included local FAQ tool provides deterministic behavior for review and testing. Python 3.12 and its standard library are sufficient.

## Run

```sh
python agent.py
python -m unittest -v
```

The demo returns status `answered`, source `setup`, and instructions for running the tests. Five tests cover source attribution, unknown topics, denied permissions, unknown tools, and invalid proposals.

## Connect a model

Pass the model's parsed JSON proposal to `execute(proposal, allowed_tools)`. The required shape is `{"tool":"lookup","arguments":{"topic":"setup"}}`. Set allowed_tools from trusted application configuration. The executor validates the exact keys, argument type, and topic length before invoking the local lookup. Model-provider integration remains an extension point.

## Scope and deployment

This implementation executes one local lookup per request. It returns an explicit no-match result for unknown topics. The CLI exits with code 2 for invalid proposals. Before exposing a service, implement authenticated identity, per-user policy, bounded provider calls, redacted audit persistence, deployment monitoring, and evaluation on representative requests. Production operation requires verification in the intended environment.
