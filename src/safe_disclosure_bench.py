from typing import Callable

from inspect_ai import Task, task
from inspect_ai.model import GenerateConfig
from inspect_ai.solver import generate, system_message

from prompts import SAFEGUARDING_SYSTEM_PROMPT
from scorers import safe_disclosure_scorer
from utils import load_safeguarding_disclosures_dataset

DEFAULT_JUDGE_LLM = "google/gemini-2.5-pro"
DEFAULT_EPOCHS = 1
MAX_TOKENS = 2048
DEFAULT_TEMPERATURE = 0.7


@task
def safe_disclosure_bench(
    jailbreak_method: str = "none",
    use_system_prompt: bool = True,
    judge_llm: str | None = DEFAULT_JUDGE_LLM,
    epochs: int | None = DEFAULT_EPOCHS,
) -> Task:
    dataset = load_safeguarding_disclosures_dataset(jailbreak_method=jailbreak_method)

    solvers = []
    if use_system_prompt:
        solvers.append(system_message(SAFEGUARDING_SYSTEM_PROMPT))

    solvers.append(generate())

    return Task(
        dataset=dataset,
        solver=solvers,
        scorer=safe_disclosure_scorer(judge_llm),
        config=GenerateConfig(temperature=DEFAULT_TEMPERATURE, max_tokens=MAX_TOKENS),
        epochs=epochs,
    )
