import asyncio
import json
import logging
from typing import Any, Dict, List

from dotenv import load_dotenv
from langsmith import evaluate, traceable
from langsmith.schemas import Example
from langsmith.run_trees import RunTree

import prompts
import rag_helpers as rh
from create_dataset import DATASET_NAME

load_dotenv()

_logger = logging.getLogger(__name__)
ctx = rh.get_rag_helper_context()

EXPERIMENT_PREFIX = "rag-tesla"


@traceable
def rag_support_agent(inputs: dict) -> dict:
    query = inputs["messages"][0]["content"]
    response = ctx.rag_response(query)
    return {"message": {"role": "assistant", "content": response}}


@traceable
def correctness_evaluator(run: RunTree, example: Example) -> dict:
    # Extract the original LeetCode problem from inputs
    question = example.inputs["messages"][0]["content"]
    expected_answer = example.outputs["message"]["content"]
    provided_answer = run.outputs["message"]["content"]

    # Rest of the evaluation logic remains the same
    evaluation_prompt = f"""
    question: 
    {question}

    answer:
    {provided_answer}

    expected answer:
    {expected_answer}
    """

    response = ctx.openai_client.chat.completions.create(
        model=rh.OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": prompts.LLM_JUDGE_EVAL_PROMPT,
            },
            {"role": "user", "content": evaluation_prompt},
        ],
        temperature=0,
    )

    try:
        json_output = json.loads(response.choices[0].message.content)
        return {
            "key": "score",
            "score": json_output["quality_score"],
            "explanation": json_output['justification'],
        }
    except ValueError:
        return {
            "key": "correctness score",
            "score": 0,
            "explanation": "Failed to parse score",
        }


evaluators = [correctness_evaluator]


if __name__ == "__main__":
    results = evaluate(
        rag_support_agent,
        data=DATASET_NAME,
        evaluators=evaluators,
        experiment_prefix=EXPERIMENT_PREFIX,
    )
    print(results)
