import os
import pandas as pd
import numpy as np

from dotenv import load_dotenv
from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity


load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def get_similarity(embedded_matrix, query_embedding, top_k: int = 3):
    sims = cosine_similarity(query_embedding, embedded_matrix)[0]

    top_indices = np.argsort(sims)[::-1][:top_k]
    for i in top_indices:
        print(f'Score: {sims[i]:.3f} | Text: {df.iloc[i]['text']}')

def embed_query(query):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )

    return np.array(response.data[0].embedding).reshape(1, -1)

if __name__ == '__main__':
    df = pd.read_parquet('embeddings.parquet')
    embedded_matrix = np.vstack(df['embedding'].values)

    query = input('Enter your query: ')
    query_embedding = embed_query(query)

    get_similarity(embedded_matrix, query_embedding, 5)

