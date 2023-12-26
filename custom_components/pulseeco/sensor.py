"""Contains the Pulse.eco sensor implementation."""

import datetime
import logging

from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, SENSOR_TYPE_MAPPING

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = datetime.timedelta(seconds=300)
PARALLEL_UPDATES = 0


async def async_setup_entry(
    hass: HomeAssistant,
    config: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Pulse.eco sensor entries."""
    sensors = await get_sensors(hass, config)
    async_add_entities(sensors, update_before_add=True)


async def get_sensors(hass: HomeAssistant, entry):
    """Calculate which sensors needs to be added in HA based on their data value types and the selected measurement stations."""
    selected_measuring_stations = entry.options.get(
        "selected_measuring_stations", entry.data.get("selected_measuring_stations")
    )
    api = hass.data[DOMAIN][entry.entry_id]["api"]

    entities = []
    for station_id in selected_measuring_stations:
        raw_data = None
        try:
            raw_data = await hass.async_add_executor_job(
                lambda station_id=station_id: api.data_raw(
                    from_=datetime.datetime.now() - datetime.timedelta(days=1),
                    to=datetime.datetime.now(),
                    sensor_id=station_id,
                )
            )
        except Exception as e:
            _LOGGER.error(
                "An error occurred while fetching raw data for station with id %s: %s",
                station_id,
                e,
            )

        if raw_data is not None and raw_data:
            measurement_data_types = {measurement["type"] for measurement in raw_data}
            for data_type in measurement_data_types:
                entities.append(
                    PulseEcoSensor(
                        hass,
                        api,
                        entry.entry_id,
                        station_id,
                        selected_measuring_stations[station_id],
                        data_type,
                        entry.data.get("city"),
                    )
                )

    return entities


class PulseEcoSensor(Entity):
    """Representation of a Pulse.eco sensor."""

    def __init__(
        self,
        hass: HomeAssistant,
        api,
        entry_id,
        station_id,
        station_description,
        data_type,
        city,
    ) -> None:
        """Initialize the PulseEcoSensor."""
        self._hass = hass
        self._api = api
        self._entry_id = entry_id
        self._station_id = station_id
        self._station_description = station_description
        self._data_type = data_type
        self._state = None
        self._last_update = None
        self._city = city

    async def async_update(self) -> None:
        """Update the state of the sensor."""
        try:
            raw_data = await self._hass.async_add_executor_job(
                self._api.data_raw,
                datetime.datetime.now() - datetime.timedelta(seconds=7200),
                datetime.datetime.now(),
                self._data_type,
                self._station_id,
            )
            # Extract the latest value from raw_data
            if raw_data:
                latest_data = raw_data[-1]
                self._state = latest_data["value"]
                self._last_update = datetime.datetime.now()
        except Exception as e:
            _LOGGER.error("An error occurred while fetching raw data: %s", e)

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return f"{self._city}_{self._station_description}_{self._data_type}"

    @property
    def unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        return f"{DOMAIN}_{self._entry_id}_{self._station_id}_{self._data_type}"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def device_class(self) -> SensorDeviceClass | None:
        """Return the device class of the sensor."""
        return SENSOR_TYPE_MAPPING[self._data_type]

    @property
    def state_class(self):
        """Return the state class of the sensor."""
        return SensorStateClass.MEASUREMENT
