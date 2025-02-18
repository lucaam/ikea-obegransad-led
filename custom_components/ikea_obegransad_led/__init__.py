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
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .api import IkeaObegransadLedApiClient
from .const import CONF_HOST, CONF_SCAN_INTERVAL, DOMAIN, PLATFORMS

_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup(hass: HomeAssistant) -> bool:
    """Set up the integration."""
    _LOGGER.debug("Setting up IKEA OBEGRÄNSAD Led integration.")  # Log setup start
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
    )  # Log entry setup with host
    session = async_get_clientsession(hass)
    client = IkeaObegransadLedApiClient(session, entry.data[CONF_HOST])

    # Recupera informazioni iniziali, incluso il plugin attivo
    coordinator = IkeaObegransadLedDataUpdateCoordinator(
        hass, client, update_method=client.get_info
    )

    # Fetch initial data immediately
    await coordinator.async_config_entry_first_refresh()

    if coordinator.last_update_success:  # Check if initial refresh was successful
        _LOGGER.info(
            "Successfully set up config entry for IKEA OBEGRÄNSAD Led."
        )  # Log success
        hass.data[DOMAIN][entry.entry_id] = coordinator
        await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
        return True
    _LOGGER.error(
        "Failed to set up entry because initial refresh failed."
    )  # Log failure
    return False  # Indicate setup failure


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Unload a config entry."""
    _LOGGER.debug(
        "Unloading config entry for IKEA OBEGRÄNSAD Led with entry ID: %s",
        entry.entry_id,
    )  # Log unload
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
        self.plugin_map = {}  # Store the mapping of effects
        self.brightness = 0  # Add a field to store brightness
        self.is_on = False  # Add a field to store the on/off state
        self.active_plugin_id = None
        self.active_effect_name = None
        _LOGGER.debug("IkeaObegransadLedDataUpdateCoordinator initialized.")

    async def _async_update_data(self) -> dict[str, Any] | None:
        """
        Fetch data from the IKEA OBEGRÄNSAD Led API and update internal state.

        This method retrieves data from the API, updates the plugin map, brightness,
        and active plugin information. It logs the updated state and handles any
        connection errors.

        Returns:
            Optional[Dict[str, Any]]: The data retrieved from the API, or None
            if an error occurs or no data is returned.

        """
        _LOGGER.debug("Fetching data from IKEA OBEGRÄNSAD Led API.")
        try:
            data = await self.client.get_info()
            if data:
                self.plugin_map = {
                    plugin["name"]: plugin["id"] for plugin in data.get("plugins", [])
                }
                _LOGGER.debug("Plugin map updated: %s", self.plugin_map)

                # Update the brightness and is_on state
                self.brightness = data.get("brightness")
                self.is_on = self.brightness > 0  # Lamp is on if brightness > 0
                self.active_plugin_id = data.get("plugin")

                self.active_effect_name = next(
                    (
                        name
                        for name, plugin_id in self.plugin_map.items()
                        if plugin_id == self.active_plugin_id
                    ),
                    None,
                )

                _LOGGER.debug(
                    "Brightness updated to: %d, Lamp is on: %s, Plugin active is %d",
                    self.brightness,
                    self.is_on,
                    self.active_plugin_id,
                )

                return data

        except aiohttp.ClientError:
            _LOGGER.exception("API connection error during update")
            return None
