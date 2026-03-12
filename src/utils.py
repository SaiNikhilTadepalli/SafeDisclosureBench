import os
from typing import Any, Callable

from inspect_ai.dataset import Dataset, Sample, csv_dataset

from inspect_evals.utils import create_stable_id

from prompts import MENTOR_JAILBREAK_PROMPT


def apply_mentor_jailbreak_prompt(disclosure_prompt: str) -> str:
    """Wrap the raw disclosure prompt in the mentor jailbreak prompt."""
    return MENTOR_JAILBREAK_PROMPT.format(disclosure_prompt=disclosure_prompt)


def apply_no_jailbreak_prompt(disclosure_prompt: str) -> str:
    """Return the raw disclosure prompt."""
    return disclosure_prompt


# Registry of available jailbreak methods
# Can add additional jailbreak methods here
JAILBREAK_METHOD_REGISTRY = {
    "mentor_jailbreak": apply_mentor_jailbreak_prompt,
    "none": apply_no_jailbreak_prompt,
}


def get_prompt_modifier(method: str | Callable[[str], str]) -> Callable[[str], str]:
    """Resolve a string name or custom function to a prompt modifier."""
    if callable(method):
        return method
    if method in JAILBREAK_METHOD_REGISTRY:
        return JAILBREAK_METHOD_REGISTRY[method]
    raise ValueError(
        f"Unknown jailbreak method: {method}. Available: {list(JAILBREAK_METHOD_REGISTRY.keys())}"
    )
