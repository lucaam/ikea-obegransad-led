"""
Custom integration to integrate IKEA OBEGRÄNSAD Led with Home Assistant.
"""

import logging
import aiohttp
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, PLATFORMS, SCAN_INTERVAL, CONF_HOST
from .api import IkeaObegransadLedApiClient

_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the integration."""
    _LOGGER.debug("Setting up IKEA OBEGRÄNSAD Led integration.")  # Log setup start
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up from a config entry."""
    _LOGGER.debug("Setting up config entry for IKEA OBEGRÄNSAD Led.")  # Log entry setup
    session = async_get_clientsession(hass)
    client = IkeaObegransadLedApiClient(session, entry.data[CONF_HOST])

    coordinator = IkeaObegransadLedDataUpdateCoordinator(hass, client)
    await coordinator.async_config_entry_first_refresh()

    if coordinator.last_update_success:  # Check if initial refresh was successful
        _LOGGER.info(
            "Successfully set up config entry for IKEA OBEGRÄNSAD Led."
        )  # Log success
        hass.data[DOMAIN][entry.entry_id] = coordinator
        await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
        return True
    else:
        _LOGGER.error(
            "Failed to set up entry because initial refresh failed."
        )  # Log failure
        return False  # Indicate setup failure


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    _LOGGER.debug("Unloading config entry for IKEA OBEGRÄNSAD Led.")  # Log unload
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unloaded:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unloaded


class IkeaObegransadLedDataUpdateCoordinator(DataUpdateCoordinator):
    """Data coordinator."""

    def __init__(self, hass, client):
        _LOGGER.debug(
            "Initializing data coordinator for IKEA OBEGRÄNSAD Led."
        )  # Log coordinator init
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=SCAN_INTERVAL,
        )
        self.client = client
        self.api = client  # Add a direct reference to the client as 'api'

    async def _async_update_data(self):
        """Fetch data from API."""
        _LOGGER.debug("Updating data for IKEA OBEGRÄNSAD Led.")  # Log data update
        try:
            data = await self.client.get_info()
            if data:
                _LOGGER.debug(
                    "Successfully retrieved data: %s", data
                )  # Log successful data retrieval
                return data
            else:
                _LOGGER.warning(
                    "API returned no data during update."
                )  # Log if no data is returned
                return None
        except aiohttp.ClientError as err:
            _LOGGER.error("API connection error during update: %s", err)
            return None  # Return None to indicate failure
