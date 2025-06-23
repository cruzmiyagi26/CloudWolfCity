import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from google.adk.tools import FunctionTool  # <-- add this import
from shared.utils import get_location_and_timezone

def get_current_time(city: str) -> str:
    _, timezone_str, error = get_location_and_timezone(city)
    if error:
        return error
    now = datetime.datetime.now(ZoneInfo(timezone_str))
    return f"The current time in {city.title()} is {now.strftime('%Y-%m-%d %H:%M:%S %Z')}."

time_tool = FunctionTool(get_current_time)  # wrap function in a tool

time_agent = Agent(
    name="time_agent",
    model="gemini-2.0-flash",
    instruction="Return the current local time for any city.",
    tools=[time_tool],  # assign tool, not raw function
)
