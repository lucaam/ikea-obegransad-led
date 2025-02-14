"""Sensor platform for IKEA OBEGRÄNSAD Led."""

import logging

from .const import DEFAULT_NAME, DOMAIN, ICON, SENSOR
from .entity import IkeaObegransadLedEntity

_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    _LOGGER.debug(
        "Setting up sensor platform for IKEA OBEGRÄNSAD Led."
    )  # Log setup start
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices([IkeaObegransadLedSensor(coordinator, entry)])


class IkeaObegransadLedSensor(IkeaObegransadLedEntity):
    """ikea_obegransad_led Sensor class."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DEFAULT_NAME}_{SENSOR}"

    @property
    def state(self):
        """Return the state."""
        if self.coordinator.data is None:  # Check if data is None
            _LOGGER.debug(
                "Coordinator data is None, returning None for state."
            )  # Log the None case
            return None  # Or return a default value like 0 if you prefer

        brightness = self.coordinator.data.get("brightness")  # No default value here
        if brightness is None:  # check if brightness is in the data
            _LOGGER.debug(
                "Brightness value not found in data, returning None for state."
            )
            return None

        _LOGGER.debug("Current brightness: %s", brightness)  # Log brightness value
        return brightness

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return ICON

    @property
    def device_class(self):
        """Return de device class of the sensor."""
        return "ikea_obegransad_led__custom_device_class"
