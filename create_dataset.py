import asyncio
import json
import logging
import random
from pathlib import Path
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

load_dotenv()

_logger = logging.getLogger(__name__)

LOCAL_CACHE_FILE = Path("./.data/question_generation_cache.json")
DATASET_NAME = "rag_evaluation_dataset"


def get_document_nodes():
    docs = SimpleDirectoryReader(
        input_files=[rh.TESLA_DOC],
        filename_as_id=True,
        file_extractor={".md": FlatReader()},
    ).load_data()
    parser = SentenceSplitter(chunk_size=2000, chunk_overlap=400)
    return parser.get_nodes_from_documents(docs)


def create_examples(ctx, nodes, num_chunks=10):
    random_chunks = random.sample(nodes, num_chunks)
    print(f"Selected {len(random_chunks)} random chunks")
    candidate_examples = []
    for node in tqdm(random_chunks):
        # Generate factual questions
        factual_response = ctx.openai_client.chat.completions.create(
            model=rh.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are a skilled question generator."},
                {
                    "role": "user",
                    "content": prompts.FACTUAL_PROMPT.format(text=node.text),
                },
            ],
            response_format={"type": "json_object"},
        )

        # Generate reasoning questions
        reasoning_response = ctx.openai_client.chat.completions.create(
            model=rh.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are a skilled question generator."},
                {
                    "role": "user",
                    "content": prompts.REASONING_PROMPT.format(text=node.text),
                },
            ],
            response_format={"type": "json_object"},
        )

        # Parse responses
        factual_questions = json.loads(factual_response.choices[0].message.content)[
            "questions"
        ]
        reasoning_questions = json.loads(reasoning_response.choices[0].message.content)[
            "questions"
        ]

        # Format and store
        for question in factual_questions + reasoning_questions:
            example = {
                "question": question["question"],
                "answer": question["answer"],
                "metadata": {
                    "chunk_id": node.node_id,
                    "question_type": question["question_type"],
                    "supporting_text": question["supporting_text"],
                    "relevance_level": question["relevance_level"],
                    "source_position": (
                        node.start_char_idx if hasattr(node, "start_char_idx") else None
                    ),
                    "filename": node.metadata.get("filename", "unknown"),
                },
            }
            candidate_examples.append(example)

    return candidate_examples


def create_dataset(ctx):
    langsmith_client = Client()
    if LOCAL_CACHE_FILE.exists():
        examples = json.loads(LOCAL_CACHE_FILE.read_text())
    else:
        nodes = get_document_nodes()
        examples = create_examples(ctx, nodes, num_chunks=10)
        LOCAL_CACHE_FILE.write_text(json.dumps(examples))

    for example in examples:
        langsmith_client.create_example(
            dataset_name=DATASET_NAME,
            inputs={"messages": {"role": "user", "content": example["question"]}},
            outputs={"messages": {"role": "assistant", "content": example["answer"]}},
            metadata=example["metadata"],
        )


if __name__ == "__main__":
    ctx = rh.get_rag_helper_context()
    create_dataset(ctx)
