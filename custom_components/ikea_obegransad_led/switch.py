"""Switch platform for IKEA OBEGRÄNSAD Led."""

from homeassistant.components.switch import SwitchEntity

from .const import DEFAULT_NAME
from .const import DOMAIN
from .const import ICON
from .const import SWITCH
from .entity import IkeaObegransadLedEntity
import logging


_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup switch platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices([IkeaObegransadLedBinarySwitch(coordinator, entry)])


class IkeaObegransadLedBinarySwitch(IkeaObegransadLedEntity, SwitchEntity):
    """ikea_obegransad_led switch class."""

    async def async_turn_on(self, **kwargs):
        """Turn on the switch."""
        await self.coordinator.api.set_brightness(
            255
        )  # Example for turning on (full brightness)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        """Turn off the switch."""
        await self.coordinator.api.set_brightness(
            0
        )  # Example for turning off (no brightness)
        await self.coordinator.async_request_refresh()

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
        # Example check, adjust based on actual response from API
        return self.coordinator.data.get("brightness", 0) > 0
