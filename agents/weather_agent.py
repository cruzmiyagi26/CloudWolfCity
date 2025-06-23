import requests
from google.adk.agents import Agent
from google.adk.tools import FunctionTool  # Import FunctionTool

# Define the weather-fetching function
def get_weather(city: str) -> str:
    try:
        res = requests.get(f"https://wttr.in/{city}?format=j1", timeout=5)
        data = res.json()
        current = data["current_condition"][0]
        desc = current["weatherDesc"][0]["value"]
        temp_c = current["temp_C"]
        temp_f = current["temp_F"]
        return f"The weather in {city.title()} is {desc}, {temp_c}°C ({temp_f}°F)."
    except Exception as e:
        return f"Could not get weather for {city}: {str(e)}"

# Wrap the get_weather function inside a FunctionTool
weather_tool = FunctionTool(get_weather)

# Define the agent using the wrapped tool
weather_agent = Agent(
    name="weather_agent",
    model="gemini-2.0-flash",
    instruction="Provide current weather for any city.",
    tools=[weather_tool],  # Use the FunctionTool here
)
