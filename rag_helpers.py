import json
import os
from dataclasses import dataclass

import openai
import weaviate
from langsmith.wrappers import wrap_openai
from llama_index.embeddings.openai import OpenAIEmbedding
from weaviate.classes.init import Auth
from weaviate.classes.query import MetadataQuery

import prompts

OPENAI_MODEL = "gpt-4o"
GPT_MINI = "gpt-4o-mini"
EMBEDDING_MODEL_NAME = "text-embedding-3-large"
COLLECTION_NAME = "TeslaCybertruckOwnersManual"
TESLA_DOC = "./.data/Tesla Cybertruck Owners Manual.md"


def get_embedding_model():
    return OpenAIEmbedding(model=EMBEDDING_MODEL_NAME)


def get_weaviate_client():
    weaviate_url = os.environ["WEAVIATE_URL"]
    weaviate_api_key = os.environ["WEAVIATE_API_KEY"]
    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=weaviate_url, auth_credentials=Auth.api_key(weaviate_api_key)
    )
    print(f"weaviate client connected: {client.is_connected()}")
    return client


def get_openai_client():
    openai_api_key = os.environ["OPENAI_API_KEY"]
    client = wrap_openai(openai.Client(api_key=openai_api_key))
    return client


def get_prompt_for_rag_query_results(*, results, query):
    context_str = "\n\n---\n\n".join(res.text for res in results)
    return f"""Answer the question using ONLY the information provided in the context below. 
Do not add any general knowledge or information not contained in the context."

Context:
{context_str}

Question: {query}

Answer:"""


@dataclass(frozen=True)
class QueryResult:
    distance: float
    text: str

    @classmethod
    def from_doc(cls, doc):
        return cls(distance=doc.metadata.distance, text=doc.properties["text"])


class RagHelperContext:
    def __init__(self, debug=False):
        self._debug = debug
        self.weaviate_client = get_weaviate_client()
        self.openai_client = get_openai_client()
        self.embedding_model = get_embedding_model()

    def meta_query(self, query, limit=3):
        response = self.openai_client.embeddings.create(
            model=EMBEDDING_MODEL_NAME, input=query
        )
        query_embedding = response.data[0].embedding
        collection = self.weaviate_client.collections.get(COLLECTION_NAME)
        similar_texts = collection.query.near_vector(
            near_vector=query_embedding,
            limit=limit,
            return_properties=["text"],
            return_metadata=MetadataQuery(distance=True),
        )
        return tuple(QueryResult.from_doc(doc) for doc in similar_texts.objects)

    def evaluate_query(self, query) -> bool:
        response = self.openai_client.chat.completions.create(
            model=GPT_MINI,
            messages=[
                {
                    "role": "system",
                    "content": prompts.CLAUDE_EVAL_PROMPT_3a_JSON,
                },
                {"role": "user", "content": query},
            ],
            temperature=0,
        )

        response_content = response.choices[0].message.content
        if self._debug:
            print(f"query: {query}\nstructured_response: {response_content}")
        structured_response = json.loads(response_content)
        return structured_response["rag_recommended"]

    def simple_response(self, query):
        response = self.openai_client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that answers questions based on the provided context.",
                },
                {"role": "user", "content": query},
            ],
            temperature=0,
        )
        return response.choices[0].message.content

    def chat_response(self, query):
        use_rag = self.evaluate_query(query)
        if not use_rag:
            if self._debug:
                print("will issue a simple response, not using RAG")
            return self.simple_response(query)
        if self._debug:
            print("will issue a RAG based response")
        return self.rag_response(query)

    def get_rag_prompt(self, prompt):
        return [
            {
                "role": "system",
                "content": prompts.CONTEXT_PROMPT,
            },
            {"role": "user", "content": prompt},
        ]

    def rag_response(self, query):
        similar_texts = self.meta_query(query)
        prompt = get_prompt_for_rag_query_results(results=similar_texts, query=query)
        response = self.openai_client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=self.get_rag_prompt(prompt),
            temperature=0,
        )
        if self._debug:
            print(f"prompt: {prompt}\n\n\n")
        return response.choices[0].message.content


def get_rag_helper_context(debug=False):
    return RagHelperContext(debug=debug)
