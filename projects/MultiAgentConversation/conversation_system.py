import asyncio
import os
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat, SelectorGroupChat
from autogen_agentchat.ui import Console
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
from autogen_ext.models.openai import OpenAIChatCompletionClient

from dotenv import load_dotenv
load_dotenv(dotenv_path='../../reference/.env')

def get_model_client():
    return OpenAIChatCompletionClient(
        model='gpt-4o-mini',
        api_key=os.environ.get('OPENAI_API_KEY'),
    )
async def team_workflow():
    print('\n' + '=' * 80)
    print('Full Stack Application')
    print('=' * 80 + '\n')

    model_client = get_model_client()

    architect = AssistantAgent(
        'architect',
        model_client=model_client,
        system_message='''You design system architecture.
        Focus on scalability, maintainability, and best practices.''',
        description='System architect who designs solutions.'
    )

    backend_dev = AssistantAgent(
        'backend_dev',
        model_client=model_client,
        system_message='''You write backend code.
        Focus on APIs, data processing, and business logic.''',
        description='Backend developer.'
    )

    frontend_dev = AssistantAgent(
        'frontend_dev',
        model_client=model_client,
        system_message='''You write frontend code.
        Focus on user interface and user experience.''',
        description='Frontend developer.'
    )

    devops = AssistantAgent(
        'devops',
        model_client=model_client,
        system_message='''You handle deployment and infrastructure.
        Provide Docker, CI/CD, and deployment strategies.
        When deployment plan is ready, say 'DEPLOYMENT_READY'.''',
        description='DevOps engineer.'
    )

    termination = (
            TextMentionTermination('DEPLOYMENT_READY') |
            MaxMessageTermination(20)
    )

    team = SelectorGroupChat(
        participants=[architect, backend_dev, frontend_dev, devops],
        model_client=model_client,
        termination_condition=termination
    )

    task = '''Design and plan a simple REST API for a todo list application.
    Include:
    - System architecture
    - Backend API endpoints
    - Frontend structure
    - Deployment strategy'''

    await Console(team.run_stream(task=task))

async def main():
    if not os.environ.get('OPENAI_API_KEY'):
        print('ERROR: OPENAI_API_KEY environment variable not set!')
        return

    await team_workflow()

    print('\n' + '=' * 80)
    print('Process Completed')
    print('=' * 80)


if __name__ == '__main__':
    asyncio.run(main())