"""Switch platform for IKEA OBEGRÄNSAD Led."""

import logging

from homeassistant.components.switch import SwitchEntity

from .const import DEFAULT_NAME, DOMAIN, ICON, SWITCH
from .entity import IkeaObegransadLedEntity

_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup switch platform."""
    _LOGGER.debug(
        "Setting up switch platform for IKEA OBEGRÄNSAD Led."
    )  # Log setup start
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices([IkeaObegransadLedBinarySwitch(coordinator, entry)])


class IkeaObegransadLedBinarySwitch(IkeaObegransadLedEntity, SwitchEntity):
    """ikea_obegransad_led switch class."""

    async def async_turn_on(self, **kwargs):
        """Turn on the switch."""
        _LOGGER.debug("Turning on switch for IKEA OBEGRÄNSAD Led.")  # Log turn on
        if self.coordinator.api:  # Check if api exists
            try:
                await self.coordinator.api.set_brightness(255)
                await self.coordinator.async_request_refresh()  # Use the refresh method
                _LOGGER.info("Successfully turned on switch.")  # Log success
            except Exception as e:
                _LOGGER.error("Error turning on switch: %s", e)  # Log error
        else:
            _LOGGER.error(
                "API not available, cannot turn on switch."
            )  # Log if API is missing

    async def async_turn_off(self, **kwargs):
        """Turn off the switch."""
        _LOGGER.debug("Turning off switch for IKEA OBEGRÄNSAD Led.")  # Log turn off
        if self.coordinator.api:  # Check if api exists
            try:
                await self.coordinator.api.set_brightness(0)
                await self.coordinator.async_request_refresh()  # Use the refresh method
                _LOGGER.info("Successfully turned off switch.")  # Log success
            except Exception as e:
                _LOGGER.error("Error turning off switch: %s", e)  # Log error
        else:
            _LOGGER.error(
                "API not available, cannot turn off switch."
            )  # Log if API is missing

    @property
    def name(self):
        """Return the name of the switch."""
        return f"{DEFAULT_NAME}_{SWITCH}"

    @property
    def icon(self):
        """Return the icon of this switch."""
        return ICON

    @property
    def is_on(self):
        """Return true if the switch is on."""
        if self.coordinator.data:  # Check if data exists
            brightness = self.coordinator.data.get("brightness", 0)
            _LOGGER.debug("Current brightness: %s", brightness)  # Log brightness value
            return brightness > 0
        return False  # or None, depending on preference
