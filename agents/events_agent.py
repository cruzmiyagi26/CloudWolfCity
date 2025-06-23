import os
import datetime
import requests
from dotenv import load_dotenv
from zoneinfo import ZoneInfo
from dateutil import parser
from shared.utils import get_location_and_timezone
from google.adk.agents import Agent
from google.adk.tools import FunctionTool

# Load environment variables
load_dotenv()

TICKETMASTER_API_KEY = os.getenv("TICKETMASTER_API_KEY")
if not TICKETMASTER_API_KEY:
    raise EnvironmentError("Missing TICKETMASTER_API_KEY in environment.")

def format_event_time(event) -> str:
    start_info = event.get("dates", {}).get("start", {})
    time_str = start_info.get("localTime")
    date_time_iso = start_info.get("dateTime")
    
    if time_str:
        try:
            time_12hr = datetime.datetime.strptime(time_str, "%H:%M").strftime("%I:%M %p").lstrip("0")
            return time_12hr
        except Exception:
            pass
    
    if date_time_iso:
        try:
            dt = parser.isoparse(date_time_iso)  # robust ISO8601 parsing
            return dt.strftime("%I:%M %p").lstrip("0")
        except Exception:
            pass
    
    return "Time TBA"

def get_events(city: str, day: str = "today") -> str:
    _, timezone_str, error = get_location_and_timezone(city)
    if error:
        return error

    now = datetime.datetime.now(ZoneInfo(timezone_str))
    try:
        if day == "today":
            start_date = now.date()
        elif day == "tomorrow":
            start_date = now.date() + datetime.timedelta(days=1)
        else:
            start_date = datetime.datetime.strptime(day, "%Y-%m-%d").date()
    except ValueError:
        return f"Invalid date format: {day}. Use YYYY-MM-DD."
    end_date = start_date

    start_utc = datetime.datetime.combine(start_date, datetime.time.min).replace(tzinfo=ZoneInfo(timezone_str)).astimezone(datetime.timezone.utc)
    end_utc = datetime.datetime.combine(end_date, datetime.time.max).replace(tzinfo=ZoneInfo(timezone_str)).astimezone(datetime.timezone.utc)

    params = {
        "apikey": TICKETMASTER_API_KEY,
        "city": city,
        "countryCode": "US",
        "startDateTime": start_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "endDateTime": end_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "size": 5
    }

    try:
        res = requests.get("https://app.ticketmaster.com/discovery/v2/events.json", params=params)
        res.raise_for_status()
        data = res.json()
    except requests.RequestException as e:
        try:
            error_info = data.get("errors", "No additional info.")
        except Exception:
            error_info = "Unknown error."
        return f"Error fetching events: {e} | Details: {error_info}"

    embedded = data.get("_embedded", {}).get("events")
    if not embedded:
        return f"No events found in {city} for {day}."

    output = f"🎟️ Events in {city.title()} on {start_date.strftime('%B %d, %Y')}:\n"
    for event in embedded:
        name = event.get("name", "Unnamed Event")
        time_12hr = format_event_time(event)
        url = event.get("url", "#")
        output += f"• {name} at {time_12hr}. [More info]({url})\n"

    return output

# Wrap into an Agent
events_tool = FunctionTool(get_events)
events_agent = Agent(
    name="events_agent",
    model="gemini-2.0-flash",
    instruction="Provide event listings for a specified city and date (e.g. 'today' or 'YYYY-MM-DD').",
    tools=[events_tool],
)
