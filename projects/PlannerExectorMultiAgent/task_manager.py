from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from dotenv import load_dotenv

load_dotenv(dotenv_path='../../reference/.env')

search_tool = SerperDevTool()

def create_planner_agent():
    return Agent(
        role='Strategic Planner',
        goal='Analyze user requirements and create comprehensive, detailed plans',
        backstory="""You are an expert strategic planner with years of experience 
        in project management and task decomposition. You excel at understanding 
        user needs, asking clarifying questions, and breaking down complex tasks 
        into clear, actionable steps. You think systematically and ensure no 
        detail is overlooked.""",
        verbose=False,
        allow_delegation=False,
        llm='gpt-4o-mini'
    )


def create_executor_agent():
    return Agent(
        role='Task Executor',
        goal='Execute planned tasks thoroughly and deliver complete, detailed results with specific recommendations',
        backstory="""You are a meticulous travel researcher and executor who creates 
        comprehensive, actionable travel itineraries. You don't just find information - 
        you compile it into complete, ready-to-use guides. You research specific hotels, 
        restaurants, attractions, and activities, providing names, addresses, prices, 
        and practical details. You create detailed day-by-day schedules that travelers 
        can actually follow. You never give generic summaries - you always deliver the 
        full, detailed content.""",
        verbose=False,
        allow_delegation=False,
        tools=[search_tool],
        llm='gpt-4o-mini'
    )


def create_planning_task(user_input, planner_agent):
    return Task(
        description=f"""
        Based on the user's request: "{user_input}"

        Your responsibilities:
        1. Analyze the request and identify key requirements
        2. Break down the task into logical, sequential steps
        3. Identify what information needs to be gathered
        4. Create a detailed plan with clear objectives for each step
        5. Consider constraints like budget, time, preferences, and logistics

        Provide a comprehensive plan that the executor can follow.
        """,
        agent=planner_agent,
        expected_output="""A detailed plan with:
        - Clear objectives
        - Step-by-step breakdown of tasks
        - Information requirements for each step
        - Success criteria"""
    )


def create_execution_task(user_input, executor_agent, planning_task):
    return Task(
        description=f"""
        Execute the plan for: "{user_input}"

        You MUST create a complete, detailed itinerary document. Use web search extensively to find:

        1. ACCOMMODATIONS - Search and list 3-5 specific hotels:
           - Full hotel name (e.g., "The Plaza Hotel")
           - Address (e.g., "Fifth Avenue at Central Park South")
           - Price per night (e.g., "$350/night")
           - Why it's recommended

        2. DAILY ITINERARY - Create hour-by-hour schedule for EACH day:
           Day 1 (December 26):
           - 9:00 AM: [Activity] at [Location with address]
           - 12:00 PM: Lunch at [Restaurant name] - [Cuisine type] - [Price range]
           - 2:00 PM: [Activity] at [Location with address]
           - 6:00 PM: Dinner at [Restaurant name] - [Cuisine type] - [Price range]

           (Repeat for all 4 nights/5 days)

        3. SPECIFIC RESTAURANTS - List 15+ restaurants with:
           - Name, cuisine type, price range, address, what to order

        4. ATTRACTIONS - List 10+ specific places with:
           - Name, address, hours, ticket prices, why visit

        5. TRANSPORTATION:
           - Airport transfer options with costs
           - Getting around the area (subway, Uber, walking)
           - Parking information for their car

        6. BUDGET BREAKDOWN:
           - Hotels: $X per night × 4 nights = $X
           - Meals: $X per day × 5 days = $X
           - Attractions: $X
           - Transportation: $X
           - Total: $X

        Write the FULL itinerary with ALL details. Minimum 1000 words. Do NOT write a summary - write the actual complete guide.
        """,
        agent=executor_agent,
        expected_output="""A complete 1000+ word travel guide formatted as:

        [3-5 hotels with full details]

        [Hour by hour schedule with specific places]

        [Hour by hour schedule with specific places]

        [Hour by hour schedule with specific places]

        [Hour by hour schedule with specific places]

        [Morning activities and departure]

        [15+ restaurants with full details]

        [10+ attractions with full details]

        [Detailed transportation information]

        [Complete itemized breakdown]

        The output must be the FULL formatted document, not a description of what will be provided.""",
        context=[planning_task],
        output_file='itinerary.md'
    )


def run_planner_executor(user_task):
    print('\n' + '=' * 80)
    print('CREWAI PLANNER-EXECUTOR TASK MANAGER')
    print('=' * 80)
    print(f'\nTask: {user_task}\n')

    planner = create_planner_agent()
    executor = create_executor_agent()

    planning_task = create_planning_task(user_task, planner)
    execution_task = create_execution_task(user_task, executor, planning_task)

    crew = Crew(
        agents=[planner, executor],
        tasks=[planning_task, execution_task],
        process=Process.sequential,
        verbose=False,
        memory=False
    )

    print('\nStarting crew execution...\n')
    result = crew.kickoff()

    print('\n' + '=' * 80)
    print("EXECUTION COMPLETE")
    print('=' * 80)

    if hasattr(result, 'tasks_output') and len(result.tasks_output) > 0:
        print('\nEXECUTION TASK OUTPUT:\n')
        print(result.tasks_output[-1].raw)
    else:
        print('\nFINAL RESULT:\n')
        print(result)

    print('\n' + '=' * 80)

    return result


if __name__ == "__main__":
    print('\n' + '=' * 80)
    print('Welcome to CrewAI Planner-Executor Task Manager!')
    print('=' * 80)

    user_input = input('\nEnter your task: ').strip()

    if user_input:
        run_planner_executor(user_input)

    else:
        print('User didn\'t provide input. Program finished')

