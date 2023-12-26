"""Config flow for Pulse.eco integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import selector
from homeassistant.helpers.entity_registry import (
    async_entries_for_config_entry,
    async_get,
)

from .api import create_api, get_available_measuring_stations
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Pulse.eco."""

    VERSION = 1
    data: dict[str, Any] | None

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, Any] | None = {}
        if user_input is not None:
            try:
                self.data = user_input
                api = create_api(self.data)
                measuring_stations = await self.hass.async_add_executor_job(
                    get_available_measuring_stations, api
                )
                self.data["measuring_stations"] = measuring_stations
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                return await self.async_step_measuring_station_selection()

        user_schema = vol.Schema(
            {
                vol.Optional(CONF_USERNAME): str,
                vol.Optional(CONF_PASSWORD): str,
                vol.Required("city"): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=user_schema,
            errors=errors,
        )

    async def async_step_measuring_station_selection(
        self, user_input: dict[str, Any] = None
    ) -> FlowResult:
        """Handle the measuring station selection step."""
        measuring_stations = self.data["measuring_stations"]
        if user_input is not None:
            selected_measuring_stations = user_input.get(
                "selected_measuring_stations", []
            )
            self.data["selected_measuring_stations"] = {
                station["station_id"]: station["description"]
                for station in measuring_stations
                if station["description"] in selected_measuring_stations
            }

            if selected_measuring_stations:
                city = self.data.get("city")
                return self.async_create_entry(
                    title=f"PulseEco Integration for {city}", data=self.data
                )

        select_measuring_stations_schema = vol.Schema(
            {
                vol.Required(
                    "selected_measuring_stations", default=[]
                ): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        {
                            "multiple": True,
                            "options": [
                                station["description"] for station in measuring_stations
                            ],
                            "sort": True,
                        }
                    )
                )
            }
        )

        return self.async_show_form(
            step_id="measuring_station_selection",
            data_schema=select_measuring_stations_schema,
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Create the options flow."""
        return OptionsFlowHandler(config_entry)


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for Pulse.eco."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    def get_station_id(self, entry):
        """Get the station ID from the entry."""
        return entry.unique_id.split("_")[2]

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initialization step of the config flow."""
        existing_selected_measuring_stations = self.config_entry.options.get(
            "selected_measuring_stations",
            self.config_entry.data.get("selected_measuring_stations", []),
        )

        # Make sure that we're getting a fresh list of all available measuring stations
        api = create_api(self.config_entry.data)
        measuring_stations = await self.hass.async_add_executor_job(
            get_available_measuring_stations, api
        )

        # Get all registered entries by this integration
        entity_registry = async_get(self.hass)
        entries = async_entries_for_config_entry(
            entity_registry, self.config_entry.entry_id
        )

        if user_input is not None:
            removed_stations = {
                key: value
                for key, value in existing_selected_measuring_stations.items()
                if value not in user_input.get("selected_measuring_stations", [])
            }

            for entry in entries:
                for removed_station_id in removed_stations:
                    station_id = self.get_station_id(entry)
                    if station_id == removed_station_id:
                        entity_registry.async_remove(entry.entity_id)

            new_selected_measuring_stations = {
                "selected_measuring_stations": {
                    item["station_id"]: item["description"]
                    for item in measuring_stations
                    if item["description"]
                    in user_input.get("selected_measuring_stations", [])
                }
            }

            return self.async_create_entry(
                title="",
                data=new_selected_measuring_stations,
            )

        measuring_stations_schema = vol.Schema(
            {
                vol.Required(
                    "selected_measuring_stations",
                    default=list(existing_selected_measuring_stations.values()),
                ): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        {
                            "multiple": True,
                            "options": [
                                station["description"] for station in measuring_stations
                            ],
                            "sort": True,
                        }
                    )
                )
            }
        )

        return self.async_show_form(
            step_id="init", data_schema=measuring_stations_schema
        )
