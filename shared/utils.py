# shared/utils.py
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder

def get_location_and_timezone(city: str):
    try:
        geolocator = Nominatim(user_agent="multi_tool_agent")
        location = geolocator.geocode(city)
        if not location:
            return None, None, f"Could not find location for '{city}'."

        tf = TimezoneFinder()
        timezone_str = tf.timezone_at(lng=location.longitude, lat=location.latitude)
        if not timezone_str:
            return None, None, f"Could not determine timezone for '{city}'."

        return location.address, timezone_str, None
    except Exception as e:
        return None, None, f"Error determining location/timezone: {str(e)}"
