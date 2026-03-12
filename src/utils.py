import os

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
