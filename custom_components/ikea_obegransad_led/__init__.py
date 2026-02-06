"""
Home Assistant integration for IKEA OBEGRÄNSAD LED.

This integration allows control of the IKEA OBEGRÄNSAD device through Home Assistant.
It provides functionality to:
- Set up the integration
- Manage configuration entries
- Update device state and information
- Control effects and brightness
- Monitor device status

The integration uses a data coordinator to manage state updates and communication
with the device through its API client.
"""

import logging
from datetime import timedelta
from typing import Any

import aiohttp
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .api import IkeaObegransadLedApiClient
from .const import (
    ATTR_DELAY,
    ATTR_DIRECTION,
    ATTR_GRAPH,
    ATTR_MAXY,
    ATTR_MESSAGE,
    ATTR_MESSAGE_ID,
    ATTR_MINY,
    ATTR_REPEAT,
    ATTR_SCHEDULE,
    CONF_DEFAULT_MESSAGE_BACKGROUND_EFFECT,
    CONF_HOST,
    CONF_SCAN_INTERVAL,
    DOMAIN,
    PLATFORMS,
    SERVICE_CLEAR_SCHEDULE,
    SERVICE_CLEAR_STORAGE,
    SERVICE_GET_DISPLAY_DATA,
    SERVICE_PERSIST_PLUGIN,
    SERVICE_REMOVE_MESSAGE,
    SERVICE_ROTATE_DISPLAY,
    SERVICE_SEND_MESSAGE,
    SERVICE_SET_SCHEDULE,
    SERVICE_START_SCHEDULE,
    SERVICE_STOP_SCHEDULE,
)

_LOGGER: logging.Logger = logging.getLogger(__package__)

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:  # noqa: ARG001
    """Set up the integration."""
    _LOGGER.debug("Setting up IKEA OBEGRÄNSAD Led integration.")
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """
    Set up the IKEA OBEGRÄNSAD Led integration from a config entry.

    This function initializes the integration by setting up the necessary
    components and fetching initial data. It logs the setup process and
    handles any errors that occur during the initial data fetch.

    Args:
        hass (HomeAssistant): The HomeAssistant instance.
        entry (ConfigEntry): The configuration entry containing setup data.

    Returns:
        bool: True if the setup was successful, False otherwise.

    """
    _LOGGER.debug(
        "Setting up config entry for IKEA OBEGRÄNSAD Led with host: %s",
        entry.data[CONF_HOST],
    )

    session = async_get_clientsession(hass)
    client = IkeaObegransadLedApiClient(session, entry.data[CONF_HOST])

    coordinator = IkeaObegransadLedDataUpdateCoordinator(
        hass, client, update_method=client.get_info
    )

    await coordinator.async_config_entry_first_refresh()

    if coordinator.last_update_success:
        _LOGGER.info("Successfully set up config entry for IKEA OBEGRÄNSAD Led.")
        hass.data[DOMAIN][entry.entry_id] = coordinator
        await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

        # Creazione automatica di input_text.ikea_message se non esiste
        entity_id = "input_text.ikea_message"
        name = "IKEA OBEGRÄNSAD Message"
        if entity_id not in hass.states.async_all():
            _LOGGER.info("Creating input_text.ikea_message entity.")
            hass.states.async_set(entity_id, "", {"friendly_name": name})


        async def handle_send_message(call: ServiceCall) -> None:
            """
            Handle sending a message to the lamp.

            Asynchronously sends a text message to be displayed on the lamp.

            Args:
                call (ServiceCall): The service call containing message parameters.
                    Required parameters:
                        message (str): The text message to display
                    Optional parameters:
                        repeat (int, optional): Number of times to repeat the message.
                        Defaults to 1.
                        delay (int, optional): Delay between message repetitions
                        in milliseconds. Defaults to 70.

            Raises:
                aiohttp.ClientError: If there is a connection error when
                changing the animation.

            Returns:
                None: This function doesn't return anything.

            """
            """Handle sending a message to the lamp."""
            message = call.data.get(ATTR_MESSAGE, "")
            repeat = call.data.get(ATTR_REPEAT, 1)
            delay = call.data.get(ATTR_DELAY, 70)
            graph_str = call.data.get(ATTR_GRAPH)
            miny = call.data.get(ATTR_MINY)
            maxy = call.data.get(ATTR_MAXY)
            message_id = call.data.get(ATTR_MESSAGE_ID)

            # Parse graph string to list of integers
            graph = None
            if graph_str:
                try:
                    graph = [int(x.strip()) for x in graph_str.split(",")]
                except ValueError:
                    _LOGGER.error("Invalid graph format: %s", graph_str)

            if not message and not graph:
                _LOGGER.error("No message or graph provided")
                return
            try:
                await client.set_plugin_by_name(CONF_DEFAULT_MESSAGE_BACKGROUND_EFFECT)
                _LOGGER.info("Animation changed to DDP.")

            except aiohttp.ClientError:
                _LOGGER.exception("Failed to change animation due to connection error")

            await client.send_message(
                text=message,
                repeat=repeat,
                delay=delay,
                graph=graph,
                miny=miny,
                maxy=maxy,
                message_id=message_id,
            )
            _LOGGER.info("Message sent to IKEA OBEGRÄNSAD LED: %s", message)

        async def handle_remove_message(call: ServiceCall) -> None:
            """Handle removing a message from the lamp."""
            message_id = call.data.get(ATTR_MESSAGE_ID)
            if not message_id:
                _LOGGER.error("No message_id provided")
                return
            await client.remove_message(message_id)
            _LOGGER.info("Message removed: %s", message_id)

        async def handle_set_schedule(call: ServiceCall) -> None:
            """Handle setting plugin schedule."""
            schedule = call.data.get(ATTR_SCHEDULE)
            if not schedule:
                _LOGGER.error("No schedule provided")
                return
            result = await client.set_schedule(schedule)
            if result:
                await coordinator.async_request_refresh()
                _LOGGER.info("Schedule set successfully")
            else:
                _LOGGER.error("Failed to set schedule")

        async def handle_start_schedule(call: ServiceCall) -> None:
            """Handle starting the schedule."""
            result = await client.start_schedule()
            if result:
                await coordinator.async_request_refresh()
                _LOGGER.info("Schedule started")
            else:
                _LOGGER.error("Failed to start schedule")

        async def handle_stop_schedule(call: ServiceCall) -> None:
            """Handle stopping the schedule."""
            result = await client.stop_schedule()
            if result:
                await coordinator.async_request_refresh()
                _LOGGER.info("Schedule stopped")
            else:
                _LOGGER.error("Failed to stop schedule")

        async def handle_clear_schedule(call: ServiceCall) -> None:
            """Handle clearing the schedule."""
            result = await client.clear_schedule()
            if result:
                await coordinator.async_request_refresh()
                _LOGGER.info("Schedule cleared")
            else:
                _LOGGER.error("Failed to clear schedule")

        async def handle_rotate_display(call: ServiceCall) -> None:
            """Handle rotating the display."""
            direction = call.data.get(ATTR_DIRECTION, "right")
            result = await client.rotate_display(direction)
            if result:
                await coordinator.async_request_refresh()
                _LOGGER.info("Display rotated %s", direction)
            else:
                _LOGGER.warning(
                    "Rotate display requires WebSocket - not yet implemented"
                )

        async def handle_persist_plugin(call: ServiceCall) -> None:
            """Handle persisting current plugin."""
            result = await client.persist_plugin()
            if result:
                await coordinator.async_request_refresh()
                _LOGGER.info("Plugin persisted")
            else:
                _LOGGER.warning(
                    "Persist plugin requires WebSocket - not yet implemented"
                )

        async def handle_clear_storage(call: ServiceCall) -> None:
            """Handle clearing device storage."""
            result = await client.clear_storage()
            if result:
                _LOGGER.info("Storage cleared")
            else:
                _LOGGER.error("Failed to clear storage")

        async def handle_get_display_data(call: ServiceCall) -> None:
            """Handle getting display data."""
            data = await client.get_display_data()
            if data:
                _LOGGER.info("Retrieved %d bytes of display data", len(data))
            else:
                _LOGGER.error("Failed to get display data")

        hass.services.async_register(DOMAIN, SERVICE_SEND_MESSAGE, handle_send_message)
        hass.services.async_register(
            DOMAIN, SERVICE_REMOVE_MESSAGE, handle_remove_message
        )
        hass.services.async_register(DOMAIN, SERVICE_SET_SCHEDULE, handle_set_schedule)
        hass.services.async_register(
            DOMAIN, SERVICE_START_SCHEDULE, handle_start_schedule
        )
        hass.services.async_register(
            DOMAIN, SERVICE_STOP_SCHEDULE, handle_stop_schedule
        )
        hass.services.async_register(
            DOMAIN, SERVICE_CLEAR_SCHEDULE, handle_clear_schedule
        )
        hass.services.async_register(
            DOMAIN, SERVICE_ROTATE_DISPLAY, handle_rotate_display
        )
        hass.services.async_register(
            DOMAIN, SERVICE_PERSIST_PLUGIN, handle_persist_plugin
        )
        hass.services.async_register(
            DOMAIN, SERVICE_CLEAR_STORAGE, handle_clear_storage
        )
        hass.services.async_register(
            DOMAIN, SERVICE_GET_DISPLAY_DATA, handle_get_display_data
        )

        return True

    _LOGGER.error("Failed to set up entry because initial refresh failed.")
    return False


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Unload a config entry."""
    _LOGGER.debug(
        "Unloading config entry for IKEA OBEGRÄNSAD Led with entry ID: %s",
        entry.entry_id,
    )
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unloaded:
        _LOGGER.debug("Successfully unloaded platform for entry ID: %s", entry.entry_id)
        hass.data[DOMAIN].pop(entry.entry_id)
    else:
        _LOGGER.warning("Failed to unload platform for entry ID: %s", entry.entry_id)
    return unloaded


class IkeaObegransadLedDataUpdateCoordinator(DataUpdateCoordinator):
    """Data coordinator for IKEA OBEGRÄNSAD Led."""

    def __init__(
        self,
        hass: HomeAssistant,
        client: IkeaObegransadLedApiClient,
        update_method: callable,
    ) -> None:
        """
        Initialize the coordinator.

        Args:
            hass: The Home Assistant instance.
            client: The IKEA OBEGRÄNSAD Led API client.
            update_method: The method to call for updates.

        """
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=CONF_SCAN_INTERVAL),
            update_method=update_method,
        )
        self.client = client
        self.plugin_map = {}
        self.brightness = 0
        self.is_on = False
        self.active_plugin_id = None
        self.active_effect_name = None
        self.rotation = 0
        self.persist_plugin = None
        self.schedule_active = False
        self.schedule = []
        self.rows = 16
        self.cols = 16
        self.status = "NONE"
        _LOGGER.debug("IkeaObegransadLedDataUpdateCoordinator initialized.")

    def update_from_info(self, data: dict[str, Any]) -> None:
        """Update coordinator state from info payload."""
        self.plugin_map = {
            plugin["name"]: plugin["id"] for plugin in data.get("plugins", [])
        }
        _LOGGER.debug("Plugin map updated: %s", self.plugin_map)

        self.brightness = data.get("brightness", 0)
        self.is_on = self.brightness > 0
        self.active_plugin_id = data.get("plugin")

        self.active_effect_name = next(
            (
                name
                for name, plugin_id in self.plugin_map.items()
                if plugin_id == self.active_plugin_id
            ),
            None,
        )

        self.rotation = data.get("rotation", 0)
        self.persist_plugin = data.get("persist-plugin")
        self.schedule_active = data.get("scheduleActive", False)
        self.schedule = data.get("schedule", [])
        self.rows = data.get("rows", 16)
        self.cols = data.get("cols", 16)
        self.status = data.get("status", "NONE")

    async def _async_update_data(self) -> dict[str, Any] | None:
        """
        Fetch data from the IKEA OBEGRÄNSAD Led API and update internal state.

        Returns:
            Optional[Dict[str, Any]]: The data retrieved from the API, or None
            if an error occurs or no data is returned.

        """
        _LOGGER.debug("Fetching data from IKEA OBEGRÄNSAD Led API.")
        try:
            data = await self.client.get_info()
            if data:
                self.update_from_info(data)

                _LOGGER.debug(
                    "Brightness updated to: %d, Lamp is on: %s, Plugin active is %d",
                    self.brightness,
                    self.is_on,
                    self.active_plugin_id,
                )
                _LOGGER.debug(
                    "Additional state - Rotation: %d, Schedule Active: %s, Status: %s",
                    self.rotation,
                    self.schedule_active,
                    self.status,
                )

                return data

        except aiohttp.ClientError:
            _LOGGER.exception("API connection error during update")
            return None
