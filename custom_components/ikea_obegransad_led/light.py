"""
The module contains the implementation of the IKEA OBEGRÄNSAD LED light integration.

It defines the IkeaObegransadLedLight class,
which represents the IKEA OBEGRÄNSAD LED light entity, and provides methods
to control the light, such as turning it on and off, setting brightness, and
applying effects.

Classes:
    IkeaObegransadLedLight: Represents the IKEA OBEGRÄNSAD LED light entity.

Functions:
    async_setup_entry: Sets up the light platform for IKEA OBEGRÄNSAD LED when
    a config entry is added.

Constants:
    DEFAULT_EFFECTS: The default list of effects for the light.
    DEFAULT_NAME: The default name of the light.
    DOMAIN: The domain of the integration.
    ICON: The icon representing the light.
    VERSION: The version of the integration.
"""

import logging
from collections.abc import Callable, Coroutine
from typing import Any

from homeassistant.components.light import ColorMode, LightEntity, LightEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DEFAULT_EFFECTS, DEFAULT_NAME, DOMAIN, ICON, VERSION

_LOGGER: logging.Logger = logging.getLogger(__package__)


class IkeaObegransadLedLight(CoordinatorEntity, LightEntity):
    """Representation of a IKEA OBEGRÄNSAD Led."""

    def __init__(self, coordinator: CoordinatorEntity, entry: ConfigEntry) -> None:
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
    def device_info(self) -> dict:
        """
        Return device information about the device.

        This method provides a dictionary containing the device's identifiers,
        name, manufacturer, model, and software version.

        Returns:
            dict: A dictionary with the following keys:
                - identifiers (set): A set containing a tuple with the
                domain and entry ID.
                - name (str): The name of the device.
                - manufacturer (str): The manufacturer of the device.
                - model (str): The model of the device.
                - sw_version (str): The software version of the device.

        """
        _LOGGER.debug("Returning device info: %s", self._name)
        return {
            "identifiers": {(DOMAIN, self.entry.entry_id)},
            "name": self._name,
            "manufacturer": "IKEA",
            "model": "OBEGRÄNSAD LED",
            "sw_version": VERSION,
        }

    @property
    def unique_id(self) -> str:
        """Return the unique ID of the entity."""
        return self.entry.entry_id

    @property
    def icon(self) -> str:
        """Return the icon of this light."""
        _LOGGER.debug("Returning icon: %s", ICON)
        return ICON

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the light on."""
        if not self._attr_effect:
            _LOGGER.debug(
                "Effect is not set. Setting effect to %s.",
                self.coordinator.active_plugin_id,
            )
            _LOGGER.debug("Effect list: %s.", self._plugin_map)
            self._attr_effect = self.coordinator.active_effect_name
            _LOGGER.debug("Set effect to %s.", self._attr_effect)

        if "brightness" in kwargs:
            self._attr_is_on = True
            await self.coordinator.client.set_brightness(kwargs["brightness"])
            self._attr_brightness = kwargs["brightness"]

        # If effect is specified, update the effect
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

    async def async_turn_off(self) -> None:
        """
        Turn the light off asynchronously.

        This method sets the light's brightness to 0, updates the internal state to
        reflect that the light is off,
        and calls the coordinator's client to turn off the light. Finally,
        it writes the updated state to Home Assistant.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            None

        """
        """Turn the light off."""
        self._last_brightness = self._attr_brightness
        self._attr_is_on = False
        self._attr_brightness = 0
        await self.coordinator.client.turn_off()

        self.async_write_ha_state()

    async def async_set_effect(self, effect_name: str) -> None:
        """
        Set the effect for the light.

        This method sets the specified effect for the light by calling the appropriate
        API or function.
        It logs the process and handles errors if the effect cannot be applied.

        Args:
            effect_name (str): The name of the effect to be set.

        Returns:
            None

        """
        if effect_name:
            _LOGGER.debug("Setting effect %s.", effect_name)
            # Call the API or function to change the effect
            effect_id = self.coordinator.plugin_map.get(effect_name)
            if effect_id is not None:
                # Assuming your API supports setting effects by ID
                success = await self.coordinator.client.set_plugin(effect_id)
                if success:
                    self._attr_effect = effect_name
                    _LOGGER.info("Effect %s successfully applied.", effect_name)
                else:
                    _LOGGER.error("Failed to apply effect %s.", effect_name)
            else:
                _LOGGER.error("Effect %s not found.", effect_name)
        else:
            _LOGGER.error("No effect name provided.")

    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        _LOGGER.debug("Access to handle coordinator update.")

        self._attr_brightness = self.coordinator.brightness
        self._attr_is_on = self.coordinator.is_on
        self._plugin_map = self.coordinator.plugin_map
        self._attr_effect_list = list(self._plugin_map.keys()) or DEFAULT_EFFECTS

        active_plugin_id = self.coordinator.active_plugin_id

        self._attr_effect = next(
            (
                name
                for name, plugin_id in self._plugin_map.items()
                if plugin_id == active_plugin_id
            ),
            None,
        )
        _LOGGER.debug("Active plugin set: %s", self._attr_effect)

        self.async_write_ha_state()


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: Callable
) -> Coroutine:
    """
    Set up the light platform for IKEA OBEGRÄNSAD LED.

    This function is called when a config entry is added. It initializes the
    light platform by creating an instance of IkeaObegransadLedLight and adding
    it to the Home Assistant entity registry.

    Args:
        hass (HomeAssistant): The Home Assistant instance.
        entry (ConfigEntry): The configuration entry for this integration.
        async_add_entities (Callable): A callback function to add entities
        to Home Assistant.

    Returns:
        Coroutine[None]: A coroutine that completes when the setup is done.

    """
    _LOGGER.debug("Setting up light platform for IKEA OBEGRÄNSAD LED.")
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([IkeaObegransadLedLight(coordinator, entry)])
    _LOGGER.info("Successfully set up light platform for IKEA OBEGRÄNSAD LED.")
