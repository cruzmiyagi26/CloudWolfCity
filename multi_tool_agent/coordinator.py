from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from agents.weather_agent import get_weather
from agents.time_agent import get_current_time
from agents.events_agent import get_events
from shared.root_agent import root_agent

def coordinator_tool(city: str) -> str:
    try:
        weather_response = get_weather(city)
        time_response = get_current_time(city)
        events_response = get_events(city)

        return f"{weather_response}\n\n{time_response}\n\n{events_response}"

    except Exception as e:
        return f"Error in fetching data: {str(e)}"

# Define the root agent at the end
root_agent = Agent(
    name="coordinator_agent",
    model="gemini-2.0-flash",
    instruction="Provide current weather, time, and today's events for a given city.",
    tools=[FunctionTool(coordinator_tool)],
)
