"""
Button platform for IKEA OBEGRÄNSAD LED.

This module provides buttons for the IKEA OBEGRÄNSAD LED integration.

Buttons provided:
- Rotate Right: Rotate display 90 degrees clockwise
- Rotate Left: Rotate display 90 degrees counter-clockwise
- Persist Plugin: Save current plugin as default on boot
- Clear Storage: Clear device storage
- Start Schedule: Start the plugin schedule
- Stop Schedule: Stop the plugin schedule
- Clear Schedule: Clear all scheduled items

Classes:
    IkeaObegransadButtonEntity: Base button entity class.
    IkeaObegransadRotateRightButton: Button to rotate display right.
    IkeaObegransadRotateLeftButton: Button to rotate display left.
    IkeaObegransadPersistPluginButton: Button to persist current plugin.
    IkeaObegransadClearStorageButton: Button to clear device storage.
    IkeaObegransadStartScheduleButton: Button to start schedule.
    IkeaObegransadStopScheduleButton: Button to stop schedule.
    IkeaObegransadClearScheduleButton: Button to clear schedule.

Functions:
    async_setup_entry: Sets up the button platform.
"""

import logging
from collections.abc import Callable

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_HOST, DOMAIN, VERSION

_LOGGER: logging.Logger = logging.getLogger(__package__)


class IkeaObegransadButtonEntity(CoordinatorEntity, ButtonEntity):
    """Base button entity for IKEA OBEGRÄNSAD LED."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: CoordinatorEntity, entry: ConfigEntry) -> None:
        """Initialize the button entity."""
        super().__init__(coordinator)
        self.entry = entry

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


class IkeaObegransadRotateRightButton(IkeaObegransadButtonEntity):
    """Button to rotate display right."""

    _attr_icon = "mdi:rotate-right"
    _attr_translation_key = "rotate_right"

    def __init__(self, coordinator: CoordinatorEntity, entry: ConfigEntry) -> None:
        """Initialize the rotate right button."""
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_rotate_right"
        self._attr_name = "Rotate Right"

    async def async_press(self) -> None:
        """Handle button press - rotate display right."""
        if self.coordinator.websocket:
            try:
                result = await self.coordinator.websocket.rotate_display("right")
                if result:
                    await self.coordinator.websocket.request_info()
                    _LOGGER.info("Display rotated right")
                else:
                    _LOGGER.error("Failed to rotate display right")
            except Exception as e:
                _LOGGER.exception("Error rotating display right: %s", e)
        else:
            _LOGGER.warning("WebSocket not initialized for rotate_right")


class IkeaObegransadRotateLeftButton(IkeaObegransadButtonEntity):
    """Button to rotate display left."""

    _attr_icon = "mdi:rotate-left"
    _attr_translation_key = "rotate_left"

    def __init__(self, coordinator: CoordinatorEntity, entry: ConfigEntry) -> None:
        """Initialize the rotate left button."""
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_rotate_left"
        self._attr_name = "Rotate Left"

    async def async_press(self) -> None:
        """Handle button press - rotate display left."""
        if self.coordinator.websocket:
            try:
                result = await self.coordinator.websocket.rotate_display("left")
                if result:
                    await self.coordinator.websocket.request_info()
                    _LOGGER.info("Display rotated left")
                else:
                    _LOGGER.error("Failed to rotate display left")
            except Exception as e:
                _LOGGER.exception("Error rotating display left: %s", e)
        else:
            _LOGGER.warning("WebSocket not initialized for rotate_left")


class IkeaObegransadPersistPluginButton(IkeaObegransadButtonEntity):
    """Button to persist current plugin as default."""

    _attr_icon = "mdi:content-save"
    _attr_translation_key = "persist_plugin"

    def __init__(self, coordinator: CoordinatorEntity, entry: ConfigEntry) -> None:
        """Initialize the persist plugin button."""
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_persist_plugin"
        self._attr_name = "Persist Plugin"

    async def async_press(self) -> None:
        """Handle button press - persist current plugin."""
        if self.coordinator.websocket:
            try:
                result = await self.coordinator.websocket.persist_plugin()
                if result:
                    await self.coordinator.websocket.request_info()
                    _LOGGER.info("Plugin persisted")
                else:
                    _LOGGER.error("Failed to persist plugin")
            except Exception as e:
                _LOGGER.exception("Error persisting plugin: %s", e)
        else:
            _LOGGER.warning("WebSocket not initialized for persist_plugin")


class IkeaObegransadClearStorageButton(IkeaObegransadButtonEntity):
    """Button to clear device storage."""

    _attr_icon = "mdi:delete-sweep"
    _attr_translation_key = "clear_storage"
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, coordinator: CoordinatorEntity, entry: ConfigEntry) -> None:
        """Initialize the clear storage button."""
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_clear_storage"
        self._attr_name = "Clear Storage"

    async def async_press(self) -> None:
        """Handle button press - clear device storage."""
        try:
            result = await self.coordinator.client.clear_storage()
            if result:
                await self.coordinator.async_request_refresh()
                _LOGGER.info("Device storage cleared")
            else:
                _LOGGER.error("Failed to clear device storage")
        except Exception as e:
            _LOGGER.exception("Error clearing device storage: %s", e)


class IkeaObegransadStartScheduleButton(IkeaObegransadButtonEntity):
    """Button to start plugin schedule."""

    _attr_icon = "mdi:play"
    _attr_translation_key = "start_schedule"

    def __init__(self, coordinator: CoordinatorEntity, entry: ConfigEntry) -> None:
        """Initialize the start schedule button."""
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_start_schedule"
        self._attr_name = "Start Schedule"

    async def async_press(self) -> None:
        """Handle button press - start schedule."""
        try:
            result = await self.coordinator.client.start_schedule()
            if result:
                await self.coordinator.async_request_refresh()
                _LOGGER.info("Schedule started")
            else:
                _LOGGER.error("Failed to start schedule")
        except Exception as e:
            _LOGGER.exception("Error starting schedule: %s", e)


class IkeaObegransadStopScheduleButton(IkeaObegransadButtonEntity):
    """Button to stop plugin schedule."""

    _attr_icon = "mdi:stop"
    _attr_translation_key = "stop_schedule"

    def __init__(self, coordinator: CoordinatorEntity, entry: ConfigEntry) -> None:
        """Initialize the stop schedule button."""
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_stop_schedule"
        self._attr_name = "Stop Schedule"

    async def async_press(self) -> None:
        """Handle button press - stop schedule."""
        try:
            result = await self.coordinator.client.stop_schedule()
            if result:
                await self.coordinator.async_request_refresh()
                _LOGGER.info("Schedule stopped")
            else:
                _LOGGER.error("Failed to stop schedule")
        except Exception as e:
            _LOGGER.exception("Error stopping schedule: %s", e)


class IkeaObegransadClearScheduleButton(IkeaObegransadButtonEntity):
    """Button to clear plugin schedule."""

    _attr_icon = "mdi:calendar-remove"
    _attr_translation_key = "clear_schedule"

    def __init__(self, coordinator: CoordinatorEntity, entry: ConfigEntry) -> None:
        """Initialize the clear schedule button."""
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_clear_schedule"
        self._attr_name = "Clear Schedule"

    async def async_press(self) -> None:
        """Handle button press - clear schedule."""
        try:
            result = await self.coordinator.client.clear_schedule()
            if result:
                await self.coordinator.async_request_refresh()
                _LOGGER.info("Schedule cleared")
            else:
                _LOGGER.error("Failed to clear schedule")
        except Exception as e:
            _LOGGER.exception("Error clearing schedule: %s", e)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: Callable
) -> None:
    """Set up the button platform for IKEA OBEGRÄNSAD LED."""
    _LOGGER.debug("Setting up button platform for IKEA OBEGRÄNSAD LED.")
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [
            IkeaObegransadRotateRightButton(coordinator, entry),
            IkeaObegransadRotateLeftButton(coordinator, entry),
            IkeaObegransadPersistPluginButton(coordinator, entry),
            IkeaObegransadClearStorageButton(coordinator, entry),
            IkeaObegransadStartScheduleButton(coordinator, entry),
            IkeaObegransadStopScheduleButton(coordinator, entry),
            IkeaObegransadClearScheduleButton(coordinator, entry),
        ]
    )
    _LOGGER.info("Successfully set up button platform for IKEA OBEGRÄNSAD LED.")
