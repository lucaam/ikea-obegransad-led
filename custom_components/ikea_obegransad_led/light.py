from homeassistant.components.light import ColorMode, LightEntity, LightEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity
import logging

from .const import DOMAIN, DEFAULT_NAME, VERSION, ICON, DEFAULT_EFFECTS

_LOGGER: logging.Logger = logging.getLogger(__package__)


class IkeaObegransadLedLight(CoordinatorEntity, LightEntity):
    """Representation of a IKEA OBEGRÄNSAD Led."""

    def __init__(self, coordinator, entry) -> None:
        """Initialize the IKEA OBEGRÄNSAD LED light."""
        super().__init__(coordinator)
        self.entry = entry
        self._name = DEFAULT_NAME
        self._attr_supported_color_modes = {ColorMode.BRIGHTNESS}
        self._attr_color_mode = ColorMode.BRIGHTNESS
        self._plugin_map = coordinator.plugin_map

        # Attributi gestiti direttamente da Home Assistant
        self._attr_is_on = coordinator.is_on
        self._attr_brightness = coordinator.brightness
        self._attr_effect = coordinator.active_effect_name
        self._attr_effect_list = DEFAULT_EFFECTS
        self._attr_supported_color_modes = {ColorMode.BRIGHTNESS}
        self._attr_color_mode = ColorMode.BRIGHTNESS
        self._attr_supported_features = LightEntityFeature.EFFECT
        self._last_brightness = 0

    @property
    def device_info(self):
        """Return device information about the device."""
        _LOGGER.debug("Returning device info: %s", self._name)
        return {
            "identifiers": {(DOMAIN, self.entry.entry_id)},
            "name": self._name,
            "manufacturer": "IKEA",
            "model": "OBEGRÄNSAD LED",
            "sw_version": VERSION,
        }

    @property
    def unique_id(self):
        """Return the unique ID of the entity."""
        return self.entry.entry_id

    @property
    def icon(self):
        """Return the icon of this light."""
        _LOGGER.debug("Returning icon: %s", ICON)
        return ICON

    async def async_turn_on(self, **kwargs):
        """Turn the light on."""
        if not self._attr_effect:
            _LOGGER.debug(
                f"Effect is not set. Setting effect to {self.coordinator.active_plugin_id}."
            )
            _LOGGER.debug(f"Effect list: {self._plugin_map}.")
            self._attr_effect = self.coordinator.active_effect_name
            _LOGGER.debug(f"Set effect to {self._attr_effect}.")

        if "brightness" in kwargs:
            self._attr_is_on = True
            await self.coordinator.client.set_brightness(kwargs["brightness"])
            self._attr_brightness = kwargs["brightness"]

        # If effect is specified, update the effelect
        elif "effect" in kwargs:
            await self.async_set_effect(kwargs["effect"])
            if not self._attr_is_on:
                if self._last_brightness:
                    await self.coordinator.client.set_brightness(self._last_brightness)
                    self._attr_brightness = self._last_brightness
                else:
                    await self.coordinator.client.turn_on()
                    self._attr_brightness = 255
                self._attr_is_on = True

        elif self._last_brightness:
            self._attr_is_on = True
            await self.coordinator.client.set_brightness(self._last_brightness)
            self._attr_brightness = self._last_brightness

        else:
            self._attr_is_on = True
            await self.coordinator.client.turn_on()
            self._attr_brightness = 255

        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Turn the light off."""
        self._last_brightness = self._attr_brightness
        self._attr_is_on = False
        self._attr_brightness = 0
        await self.coordinator.client.turn_off()

        self.async_write_ha_state()

    async def async_set_effect(self, effect_name):
        """Set the effect for the light."""
        if effect_name:
            _LOGGER.debug(f"Setting effect {effect_name}.")
            # Call the API or function to change the effect
            effect_id = self.coordinator.plugin_map.get(effect_name)
            if effect_id is not None:
                # Assuming your API supports setting effects by ID
                success = await self.coordinator.client.set_plugin(effect_id)
                if success:
                    self._attr_effect = effect_name
                    _LOGGER.info(f"Effect {effect_name} successfully applied.")
                else:
                    _LOGGER.error(f"Failed to apply effect {effect_name}.")
            else:
                _LOGGER.error(f"Effect {effect_name} not found.")
        else:
            _LOGGER.error("No effect name provided.")

    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        _LOGGER.debug("Access to handle coordinator update.")

        # The coordinator provides the latest data about the device (including status, effects, etc.)
        # await self.coordinator.async_request_refresh()

        self._attr_brightness = self.coordinator.brightness
        self._attr_is_on = self.coordinator.is_on
        self._plugin_map = self.coordinator.plugin_map
        self._attr_effect_list = list(self._plugin_map.keys()) or DEFAULT_EFFECTS

        active_plugin_id = self.coordinator.active_plugin_id
        # if active_plugin_id:

        self._attr_effect = next(
            (name for name, id in self._plugin_map.items() if id == active_plugin_id),
            None,
        )
        _LOGGER.debug("Active plugin set: %s", self._attr_effect)
        # else:
        # _LOGGER.debug("No active plugin set.")

        self.async_write_ha_state()


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
):
    """Setup light platform."""
    _LOGGER.debug("Setting up light platform for IKEA OBEGRÄNSAD LED.")
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([IkeaObegransadLedLight(coordinator, entry)])
