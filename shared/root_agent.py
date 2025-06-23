from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from agents.weather_agent import weather_agent
from agents.time_agent import time_agent
from agents.events_agent import events_agent

def coordinator_tool(city: str) -> str:
    def call_tool(tool, city):
        if callable(tool):
            return tool(city)
        elif hasattr(tool, 'func') and callable(tool.func):
            return tool.func(city)
        else:
            raise ValueError("Tool is not callable")
    
    weather_response = call_tool(weather_agent.tools[0], city)
    events_response = call_tool(events_agent.tools[0], city)
    time_response = call_tool(time_agent.tools[0], city)

    return f"{weather_response}\n\n{events_response}\n\n{time_response}"

coordinator_function = FunctionTool(coordinator_tool)

root_agent = Agent(
    name="coordinator_agent",
    model="gemini-2.0-flash",
    instruction="Provide current time, weather, and today's events for a given city.",
    tools=[coordinator_function],
)

def run(query: str) -> str:
    if not query.strip():
        return "City is required."
    try:
        return coordinator_tool(query.strip())
    except Exception as e:
        return f"Error: {e}"
