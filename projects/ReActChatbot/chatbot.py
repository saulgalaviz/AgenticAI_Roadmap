from langchain_openai import ChatOpenAI
from tools import AGENT_TOOLS
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

from dotenv import load_dotenv
load_dotenv(dotenv_path='../../reference/.env')

llm = ChatOpenAI(model='gpt-4o-mini', temperature=1.2)

checkpointer = InMemorySaver()

agent = create_agent(
    model=llm,
    tools=AGENT_TOOLS,
    system_prompt='You are a reasoning chatbot. You bounce back ideas based on the response you receive, critiquing deeply.',
    debug=True,
    checkpointer=checkpointer
)

print('Reasoning chatbot! Please pretend I\'m your close friend :) (type \'exit\' to quit)')
thread_config = {'configurable': {'thread_id': 'default_thread'}}

while True:
    user_input = input('You: ')
    if user_input.lower() in {'exit', 'quit'}:
        break

    user_command = {'messages': [{'role': 'user', 'content': user_input}]}
    result = agent.invoke(user_command, thread_config)

    messages = result.get('messages', [])
    if messages:
        output_text = messages[-1].content
    else:
        output_text = 'No response generated.'

    print('AI:', output_text)