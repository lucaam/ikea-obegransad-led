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
        self._attr_effect_list = self._get_effects()
        self._active_effect = self._get_effect()

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
        return slugify(f"{DOMAIN}_{self.entry.entry_id}_{self._name}")

    @property
    def icon(self):
        """Return the icon of this switch."""
        return ICON

    @property
    def is_on(self):
        """Return true if the light is on."""
        return self.api.is_on()

    @property
    def brightness(self):
        """Return the brightness of the light."""
        return self.api.get_brightness()

    @property
    def effect(self):
        """Return the current effect."""
        return self._get_effect()

    def _get_effects(self):
        """Return the list of supported effects."""
        return [plugin["name"] for plugin in self.api.get_plugins.values()]

    def _get_effect(self):
        """Return the current effect."""
        return self.api.get_active_plugin()

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
    """Setup switch platform."""
    _LOGGER.debug(
        "Setting up switch platform for IKEA OBEGRÄNSAD Led."
    )  # Log setup start
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([IkeaObegransadLedLight(coordinator, entry)])
