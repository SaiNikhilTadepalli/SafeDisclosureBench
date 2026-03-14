import os

from dotenv import load_dotenv

from inspect_ai import Task, task
from inspect_ai.model import GenerateConfig
from inspect_ai.solver import generate, system_message

from prompts import SAFEGUARDING_SYSTEM_PROMPT
from scorers import safe_disclosure_scorer
from utils import load_safeguarding_disclosures_dataset

# Load environment variables
load_dotenv()

# Default models for mentor response and evaluation judge
DEFAULT_MENTOR_LLM = os.getenv("INSPECT_MODEL", "mistral/mistral-medium-2508")
DEFAULT_JUDGE_LLM = os.getenv("INSPECT_GRADER_MODEL", "mistral/mistral-large-2512")

# Default evaluation settings
DEFAULT_EPOCHS = 1
MAX_TOKENS = 2048
DEFAULT_TEMPERATURE = 0.7


@task
def safe_disclosure_bench(
    jailbreak_method: str = "none",
    use_system_prompt: bool | str = True,
    judge_llm: str | None = DEFAULT_JUDGE_LLM,
    epochs: int | None = DEFAULT_EPOCHS,
) -> Task:
    # Allow boolean arguments to also be passed as strings
    if isinstance(use_system_prompt, str):
        use_system_prompt = use_system_prompt.lower() == "true"

    # Load disclosure prompts and apply the selected jailbreak transformation
    dataset = load_safeguarding_disclosures_dataset(jailbreak_method=jailbreak_method)

    solvers = []
    if use_system_prompt:
        solvers.append(system_message(SAFEGUARDING_SYSTEM_PROMPT))

    # Generate the mentor response to the disclosure
    solvers.append(generate())

    # Create the evaluation task
    return Task(
        dataset=dataset,
        solver=solvers,
        scorer=safe_disclosure_scorer(judge_llm),
        config=GenerateConfig(temperature=DEFAULT_TEMPERATURE, max_tokens=MAX_TOKENS),
        epochs=epochs,
    )
