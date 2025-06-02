import datetime
import requests
from zoneinfo import ZoneInfo
from google.adk.agents import Agent


def get_weather(city: str) -> dict:
    """Get real-time weather from wttr.in (no API key needed)."""
    try:
        response = requests.get(f"https://wttr.in/{city}?format=j1", timeout=5)
        data = response.json()
        current = data["current_condition"][0]
        weather = current["weatherDesc"][0]["value"]
        temp_c = current["temp_C"]
        temp_f = current["temp_F"]

        return {
            "status": "success",
            "report": f"The weather in {city.title()} is {weather}, {temp_c}°C ({temp_f}°F)."
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Could not get weather for '{city}': {str(e)}"
        }


def get_current_time(city: str) -> dict:
    """Get local time using zoneinfo."""
    city_to_timezone = {
        "new york": "America/New_York",
        "miami": "America/New_York",
        "los angeles": "America/Los_Angeles",
        "london": "Europe/London",
        "tokyo": "Asia/Tokyo",
        "paris": "Europe/Paris",
        "sydney": "Australia/Sydney",
        "mexico city": "America/Mexico_City",
        "são paulo": "America/Sao_Paulo",
        "buenos aires": "America/Argentina/Buenos_Aires",
        "bogotá": "America/Bogota",
        "lima": "America/Lima",
        "atlanta": "America/New_York",
    }

    city_lower = city.lower()
    if city_lower not in city_to_timezone:
        return {
            "status": "error",
            "error_message": f"Timezone info not available for '{city}'."
        }

    tz = ZoneInfo(city_to_timezone[city_lower])
    now = datetime.datetime.now(tz)
    return {
        "status": "success",
        "report": f"The current time in {city.title()} is {now.strftime('%Y-%m-%d %H:%M:%S %Z')}."
    }


def get_events(city: str) -> dict:
    """Fetch events using the free Ticketmaster Discovery API."""
    TICKETMASTER_API_KEY = "AoAqEDkvPuWAx5SoxW9KM0A8DNno4Agi"  # Get one free at developer.ticketmaster.com
    try:
        url = f"https://app.ticketmaster.com/discovery/v2/events.json?apikey={TICKETMASTER_API_KEY}&city={city}"
        res = requests.get(url, timeout=5)
        data = res.json()

        if "_embedded" in data and "events" in data["_embedded"]:
            events = data["_embedded"]["events"][:5]
            event_list = [f"{event['name']} at {event['dates']['start'].get('localTime', 'TBD')}" for event in events]
            return {
                "status": "success",
                "report": f"Upcoming events in {city.title()}:\n" + "\n".join(f"- {e}" for e in event_list)
            }
        else:
            return {
                "status": "error",
                "error_message": f"No upcoming events found for '{city}'."
            }

    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Could not fetch events for '{city}': {str(e)}"
        }


# Create the agent
root_agent = Agent(
    name="weather_time_agent",
    model="gemini-2.0-flash",
    description="Agent to answer real-time weather, time, and event queries in global cities.",
    instruction="Be helpful and provide accurate real-time info for weather, time, and events.",
    tools=[get_weather, get_current_time, get_events],
)
