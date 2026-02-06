"""
Select platform for IKEA OBEGRÄNSAD LED.

This module provides select entities for the IKEA OBEGRÄNSAD LED integration.

Select entities provided:
- Plugin: Select active plugin from dropdown list

Classes:
    IkeaObegransadPluginSelect: Select entity for choosing active plugin.

Functions:
    async_setup_entry: Sets up the select platform.
"""

import logging
from collections.abc import Callable

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_HOST, DOMAIN, VERSION

_LOGGER: logging.Logger = logging.getLogger(__package__)


class IkeaObegransadPluginSelect(CoordinatorEntity, SelectEntity):
    """Select entity for choosing active plugin."""

    _attr_has_entity_name = True
    _attr_icon = "mdi:format-list-bulleted"
    _attr_translation_key = "plugin"

    def __init__(self, coordinator: CoordinatorEntity, entry: ConfigEntry) -> None:
        """Initialize the plugin select entity."""
        super().__init__(coordinator)
        self.entry = entry
        self._attr_unique_id = f"{entry.entry_id}_plugin_select"
        self._attr_name = "Plugin"

    @property
    def current_option(self) -> str | None:
        """Return the currently selected plugin."""
        return self.coordinator.active_effect_name

    @property
    def options(self) -> list[str]:
        """Return list of available plugins."""
        return list(self.coordinator.plugin_map.keys())

    async def async_select_option(self, option: str) -> None:
        """Change the selected plugin."""
        try:
            result = await self.coordinator.client.set_plugin_by_name(option)
            if result:
                await self.coordinator.async_request_refresh()
                _LOGGER.info("Plugin changed to: %s", option)
            else:
                _LOGGER.error("Failed to change plugin to: %s", option)
        except Exception as e:
            _LOGGER.exception("Error changing plugin to %s: %s", option, e)

    @property
    def device_info(self) -> dict:
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self.entry.entry_id)},
            "name": "Ikea OBEGRÄNSAD LED Wall Light",
            "manufacturer": "IKEA",
            "model": "OBEGRÄNSAD LED Wall Light",
            "sw_version": VERSION,
            "configuration_url": f"http://{self.entry.data[CONF_HOST]}",
        }

    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        _LOGGER.debug(
            "Plugin select update - current: %s, available: %s",
            self.coordinator.active_effect_name,
            list(self.coordinator.plugin_map.keys()),
        )
        self.async_write_ha_state()


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: Callable
) -> None:
    """Set up the select platform for IKEA OBEGRÄNSAD LED."""
    _LOGGER.debug("Setting up select platform for IKEA OBEGRÄNSAD LED.")
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([IkeaObegransadPluginSelect(coordinator, entry)])
    _LOGGER.info("Successfully set up select platform for IKEA OBEGRÄNSAD LED.")
