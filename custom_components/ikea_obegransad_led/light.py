"""Light module for Custom Ambilight integration."""

from homeassistant.components.light import ColorMode, LightEntity, LightEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import slugify

import logging

from .const import DOMAIN, DEFAULT_NAME, VERSION, ICON

_LOGGER: logging.Logger = logging.getLogger(__package__)


class IkeaObegransadLedLight(CoordinatorEntity, LightEntity):
    """Representation of a IKEA OBEGRÄNSAD Led."""

    def __init__(self, coordinator, entry) -> None:
        # """Initialize the wall light."""
        super().__init__(coordinator)
        self.api = coordinator.api
        self.entry = entry
        self._name = DEFAULT_NAME
        self._attr_supported_color_modes = {ColorMode.BRIGHTNESS}
        self._attr_color_mode = ColorMode.BRIGHTNESS
        self._attr_supported_plugins = LightEntityFeature.EFFECT
        self._attr_effect_list = [
            "Draw",
            "Breakout",
            "Snake",
            "GameOfLife",
            "Stars",
            "Lines",
            "Circle",
            "Rain",
            "Firework",
            "Big Clock",
            "Clock",
            "PongClock",
            "Ticking Clock",
            "Weather",
            "Animation",
            "DDP",
        ]
        self._active_effect = coordinator.data.get("plugin")
        self._brightness = coordinator.data.get("brightness")

    @property
    def device_info(self):
        """Return device information about the device."""
        return {
            "identifiers": {(DOMAIN, self.entry.entry_id)},
            "name": self._name,
            "manufacturer": "IKEA",  # Replace with actual manufacturer if known
            "model": "OBEGRÄNSAD LED",  # Replace with actual model if known
            "sw_version": VERSION,  # Replace with actual version if known
        }

    @property
    def unique_id(self):
        """Return the unique ID of the entity."""
        return slugify(f"{self._name}")

    @property
    def icon(self):
        """Return the icon of this switch."""
        return ICON

    @property
    def is_on(self):
        """Return true if the light is on."""
        return self._brightness > 0

    @property
    def brightness(self) -> int:
        """Return the brightness of the light."""
        return self._brightness

    @brightness.setter
    async def brightness(self, value: int) -> None:
        """Set the brightness of the light."""
        if value < 0 or value > 255:
            raise ValueError("Brightness must be between 0 and 255")
        self._brightness = value
        await self._set_brightness(value)

    async def _set_brightness(self, value: int) -> None:
        """Send the brightness level to the physical light."""
        await self.api.set_brightness(value)

    @property
    def effect(self):
        """Return the current effect."""
        return self._get_effect()

    async def _get_effects(self):
        """Return the list of supported effects."""
        plugins = await self.api.get_plugins()
        return [plugin["name"] for plugin in plugins.values()]

    async def _get_effect(self):
        """Return the current effect."""
        active_plugin = await self.api.get_active_plugin()
        return active_plugin

    async def async_turn_on(self):
        """Turn the light on."""
        await self.coordinator.async_refresh()
        await self.api.turn_on()
        await self.coordinator.async_refresh()

    async def async_turn_off(self):
        """Turn the light off."""
        await self.coordinator.async_refresh()
        await self.api.turn_off()
        await self.coordinator.async_refresh()


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
):
    """Setup light platform."""
    _LOGGER.debug("Setting up light platform for IKEA OBEGRÄNSAD Led.")
    # Ottieni il coordinator
    coordinator = hass.data[DOMAIN][entry.entry_id]
    # Aggiungi le entità alla piattaforma
    async_add_entities([IkeaObegransadLedLight(coordinator, entry)])
