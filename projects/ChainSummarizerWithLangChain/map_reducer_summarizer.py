import asyncio
from dotenv import load_dotenv
load_dotenv(dotenv_path='../../reference/.env')

from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

def load_document():
    file_path = '../../reference/punching_down_podcast_episode_18.txt'

    with open(file_path, 'r') as file:
        return file.read()


def split_into_chunks(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=200,
    )
    return splitter.create_documents([text])


map_prompt = PromptTemplate.from_template('''
Write a concise summary of the following document chunk:

{chunk}

Summary:
''')


reduce_prompt = PromptTemplate.from_template('''
Combine the following partial summaries into a single cohesive summary:

{summaries}

Final Summary:
''')


model = ChatOpenAI(model='gpt-4o-mini')
parser = StrOutputParser()

map_chain = map_prompt | model | parser
reduce_chain = reduce_prompt | model | parser


async def summarize_chunk(chunk):
    return await map_chain.ainvoke({'chunk': chunk})

async def map_reduce_summarize(text):
    docs = split_into_chunks(text)

    partial_summaries = await asyncio.gather(
        *(summarize_chunk(doc.page_content) for doc in docs)
    )

    combined = '\n\n'.join(partial_summaries)
    final_summary = await reduce_chain.ainvoke({'summaries': combined})
    return final_summary


if __name__ == '__main__':
    full_text = load_document()
    summary = asyncio.run(map_reduce_summarize(full_text))

    print('\n=== FINAL SUMMARY ===\n')
    print(summary)
