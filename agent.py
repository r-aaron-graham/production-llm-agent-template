"""Execute a validated model-proposed tool call against a local FAQ."""
import argparse
import json

FAQ = {"setup": "Run python -m unittest -v to verify this template.",
       "privacy": "This example processes requests locally."}


def execute(proposal, allowed_tools):
    if not isinstance(proposal, dict) or set(proposal) != {"tool", "arguments"}:
        raise ValueError("Expected tool and arguments fields")
    tool = proposal["tool"]
    if not isinstance(tool, str) or tool not in {"lookup"} or tool not in allowed_tools:
        raise ValueError("Tool is not permitted")
    arguments = proposal["arguments"]
    if not isinstance(arguments, dict) or set(arguments) != {"topic"}:
        raise ValueError("Expected a topic argument")
    topic = arguments["topic"]
    if not isinstance(topic, str) or len(topic) > 100:
        raise ValueError("Topic must be a string of at most 100 characters")
    text = FAQ.get(topic)
    return {"status": "answered" if text else "no_match",
            "answer": text, "source": topic if text else None}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--proposal", default='{"tool":"lookup","arguments":{"topic":"setup"}}')
    args = parser.parse_args()
    try:
        result = execute(json.loads(args.proposal), {"lookup"})
    except ValueError as exc:
        parser.exit(2, f"Invalid proposal: {exc}\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
