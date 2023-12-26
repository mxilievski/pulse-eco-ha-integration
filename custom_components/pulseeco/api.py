"""Provides common functions for the PulseEcoAPI."""
from pulseeco import PulseEcoAPI
import requests


def get_available_measuring_stations(api: PulseEcoAPI):
    """Get a list of available measuring stations from the PulseEcoAPI.

    Args:
        api (PulseEcoAPI): The PulseEcoAPI instance.

    Returns:
        list: A list of measuring stations.
    """
    active_statuses = {
        "ACTIVE",
        "ACTIVE_UNCONFIRMED",
        "NOT_CLAIMED",
        "NOT_CLAIMED_UNCONFIRMED",
    }

    return [
        {
            "station_id": station["sensorId"],
            "description": station["description"],
        }
        for station in api.sensors()
        if station["status"] in active_statuses
    ]


def create_api(data: dict) -> PulseEcoAPI:
    """Create a PulseEcoAPI instance based on the provided data."""
    city = data.get("city")
    username = data.get("username")
    password = data.get("password")
    auth = (username, password) if username and password else None
    session = requests.Session()
    session.mount("https://", requests.adapters.HTTPAdapter(pool_maxsize=50))
    session.mount("http://", requests.adapters.HTTPAdapter(pool_maxsize=50))

    return PulseEcoAPI(city_name=city, session=session, auth=auth)
