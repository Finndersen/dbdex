import argparse
from collections import defaultdict
from typing import get_args

from pydantic_ai.models import KnownModelName


def format_model_options(model_options: list[str]) -> str:
    # Group models by provider
    grouped: defaultdict[str, list[str]] = defaultdict(list)
    for item in model_options:
        if item == "test":
            continue
        provider, model = item.split(":")
        grouped[provider].append(model)

    # Format the output
    formatted_lines = [f"- {provider}: {', '.join(models)}" for provider, models in grouped.items()]
    return "\n".join(formatted_lines)


def get_cli_args() -> argparse.Namespace:
    MODEL_OPTIONS = [
        model_name
        for model_name in get_args(KnownModelName)
        if model_name != "test" and not model_name.startswith("google-vertex")
    ]

    parser = argparse.ArgumentParser(description="ChatDB CLI", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        "--db-uri",
        type=str,
        help="Database connection URI",
    )
    parser.add_argument(
        "--model",
        type=str,
        required=True,
        help="Name of the LLM model to use, in format provider:model (e.g. openai:gpt-4). "
        "Choices (not exhaustive, more may be supported):\n" + format_model_options(MODEL_OPTIONS),
        metavar="PROVIDER:MODEL",
        # Don't strictly enforce choices since new models may be added
    )
    parser.add_argument(
        "--api-key",
        type=str,
        required=True,
        help="API key for the model service",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Display logging output in console",
    )
    parser.add_argument(
        "--max-return-values",
        type=int,
        default=200,
        help="Maximum number of values (cells) to return to the LLM from a DB query",
    )

    args = parser.parse_args()

    return args
