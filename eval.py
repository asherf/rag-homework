import asyncio
import json
import logging
import random
from typing import Any, Dict, List

from dotenv import load_dotenv
from langsmith import Client, evaluate, traceable
from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.readers.file import FlatReader
from openai import OpenAI
from tqdm import tqdm

import prompts
import rag_helpers as rh
from create_dataset import DATASET_NAME

load_dotenv()

_logger = logging.getLogger(__name__)
ctx = rh.get_rag_helper_context()

EXPERIMENT_PREFIX = "rag-tesla"


@traceable
def rag_support_agent(inputs: dict) -> dict:
    return {
        "message": {"role": "assistant", "content": ctx.rag_response(inputs["query"])}
    }


@traceable
def correctness_evaluator(run, example) -> dict:
    # Extract the original LeetCode problem from inputs
    question = run.inputs
    provided_answer = run.outputs
    expected_answer = example

    # Rest of the evaluation logic remains the same
    evaluation_prompt = f"""
    question: 
    {question}

    answer:
    {provided_answer}

    expected answer:
    {expected_answer}
    """

    async def get_eval_completion():
        response = await ctx.openai_client.chat.completions.create(
            model=rh.MAIN_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": prompts.LLM_JUDGE_EVAL_PROMPT,
                },
                {"role": "user", "content": evaluation_prompt},
            ],
            temperature=0,
        )
        return response

    response = asyncio.run(get_eval_completion())
    try:
        json_output = json.loads(response.choices[0].message.content)
        return {
            "key": "score",
            "score": json_output["total_score"],
            "explanation": json_output,
        }
    except ValueError:
        return {
            "key": "correctness score",
            "score": 0,
            "explanation": "Failed to parse score",
        }


evaluators = [correctness_evaluator]


results = evaluate(
    rag_support_agent,
    data=DATASET_NAME,
    evaluators=evaluators,
    experiment_prefix=EXPERIMENT_PREFIX,
)
