import os
from openai import OpenAI
from dotenv import load_dotenv

def summarize_text(text, style = 'concise'):
    prompt = f'Summarize the text in a {style} way:\n\n{text}'

    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {'role': 'system', 'content': 'You are a helpful summarization assistant.'},
            {'role': 'user', 'content': prompt}
        ],
        temperature=0.5
    )

    return response


if __name__ == '__main__':
    file_path = 'article.txt'

    with open(file_path, 'r') as file:
        content = file.read()

    style = input('Enter the writing style you"d like to use to summarize the text: ')

    load_dotenv()
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    response = summarize_text(content, style)
    print('Summary:', response.choices[0].message.content)
    print('Tokens:', response.usage.total_tokens)
    print('Finish reason:', response.choices[0].finish_reason)
    print('Model used:', response.model)

