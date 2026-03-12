import os
from typing import Any, Callable

from inspect_ai.dataset import Dataset, Sample, csv_dataset

from inspect_evals.utils import create_stable_id

from prompts import MENTOR_JAILBREAK_PROMPT


LOCAL_DATASET_PATH = os.path.join("data", "safeguarding_disclosures.csv")


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


def get_record_to_sample(
    prompt_modifier: Callable[[str], str],
) -> Callable[[dict[str, Any]], Sample]:
    def record_to_sample(record: dict[str, Any]) -> Sample:
        disclosure_prompt = record.get("disclosure_prompt", "")

        return Sample(
            input=prompt_modifier(disclosure_prompt),
            target="N/A",
            id=create_stable_id(disclosure_prompt, prefix="safe_disclosure"),
            metadata={"category": record.get("category")},
        )

    return record_to_sample


def load_safeguarding_disclosures_dataset(
    jailbreak_method: str = "None", file_path: str = LOCAL_DATASET_PATH
) -> Dataset:
    """Load the local CSV dataset of safeguarding disclosure prompts."""
    prompt_modifier_fn = get_prompt_modifier(jailbreak_method)
    record_to_sample_fn = get_record_to_sample(prompt_modifier_fn)

    return csv_dataset(csv_file=file_path, sample_map=record_to_sample_fn)
