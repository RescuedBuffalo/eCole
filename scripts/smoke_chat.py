"""Send a quick chat to verify routing."""
import argparse
import json

from ecole.backend.models.llm import llm


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("message", help="User message")
    parser.add_argument(
        "--task",
        default='{"type":"general","expected_context_tokens":100,"expected_output_tokens":200}',
        help="Task JSON",
    )
    args = parser.parse_args()
    task = json.loads(args.task)
    messages = [
        {"role": "system", "content": "You are eCole."},
        {"role": "user", "content": args.message},
    ]
    reply = llm.generate(task, messages)
    print(reply)


if __name__ == "__main__":
    main()
