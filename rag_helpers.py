import os
from dataclasses import dataclass
import openai
from llama_index.embeddings.openai import OpenAIEmbedding

# from openai import OpenAI
import weaviate
from weaviate.classes.init import Auth
from weaviate.classes.query import MetadataQuery


OPENAI_MODEL = "gpt-4o"
EMBEDDING_MODEL_NAME = "text-embedding-3-large"
COLLECTION_NAME = "TeslaCybertruckOwnersManual"


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
    client = openai.Client(api_key=openai_api_key)
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
    def __init__(self):
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

    def chat_response(self, query, debug=False):
        similar_texts = self.meta_query(query)
        prompt = get_prompt_for_rag_query_results(results=similar_texts, query=query)
        response = self.openai_client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that answers questions based on the provided context.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0,
        )
        if debug:
            print(f"prompt: {prompt}\n\n\n")
        return response.choices[0].message.content


def get_rag_helper_context():
    return RagHelperContext()
