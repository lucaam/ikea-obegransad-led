"""
Binary sensor platform for IKEA OBEGRÄNSAD LED.

This module provides binary sensors for the IKEA OBEGRÄNSAD LED integration.
Currently supports:
- Schedule Active sensor: indicates whether the plugin scheduler is active

Classes:
    IkeaObegransadScheduleSensor: Binary sensor for schedule status.

Functions:
    async_setup_entry: Sets up the binary sensor platform.
"""

import logging
from collections.abc import Callable

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_HOST, DOMAIN, VERSION

_LOGGER: logging.Logger = logging.getLogger(__package__)


class IkeaObegransadScheduleSensor(CoordinatorEntity, BinarySensorEntity):
    """Binary sensor for schedule status."""

    _attr_has_entity_name = True
    _attr_device_class = BinarySensorDeviceClass.RUNNING

    def __init__(self, coordinator: CoordinatorEntity, entry: ConfigEntry) -> None:
        """Initialize the schedule sensor."""
        super().__init__(coordinator)
        self.entry = entry
        self._attr_unique_id = f"{entry.entry_id}_schedule_active"
        self._attr_name = "Schedule Active"

    @property
    def is_on(self) -> bool:
        """Return true if the schedule is active."""
        return self.coordinator.schedule_active

    @property
    def extra_state_attributes(self) -> dict:
        """Return additional state attributes."""
        return {
            "schedule": self.coordinator.schedule,
            "schedule_count": len(self.coordinator.schedule),
        }

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
        _LOGGER.debug("Schedule sensor update: %s", self.coordinator.schedule_active)
        self.async_write_ha_state()


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: Callable
) -> None:
    """Set up the binary sensor platform for IKEA OBEGRÄNSAD LED."""
    _LOGGER.debug("Setting up binary sensor platform for IKEA OBEGRÄNSAD LED.")
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([IkeaObegransadScheduleSensor(coordinator, entry)])
    _LOGGER.info("Successfully set up binary sensor platform for IKEA OBEGRÄNSAD LED.")
