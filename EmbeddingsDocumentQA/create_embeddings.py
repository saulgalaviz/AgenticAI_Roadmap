import os
import pandas as pd

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def chunk_text(text, max_tokens=500, overlap=50):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + max_tokens
        chunk = ' '.join(words[start:end])
        chunks.append(chunk)
        start += max_tokens - overlap

    return chunks

def embed_text(docs):
    response = client.embeddings.create(
        model='text-embedding-3-small',
        input=docs
    )

    print(response.data)

    embeddings = [item.embedding for item in response.data]

    df = pd.DataFrame({'text': docs, 'embedding': embeddings})
    df.to_parquet('embeddings.parquet')


if __name__ == '__main__':
    file_path = 'star_wars_lore.txt'

    with open(file_path, 'r') as file:
        content = file.read()

    docs = chunk_text(content, max_tokens=500, overlap=50)
    print(f"Created {len(docs)} chunks for embedding.")

    embed_text(docs)



