"""
Sensor platform for IKEA OBEGRÄNSAD LED.

This module provides sensors for the IKEA OBEGRÄNSAD LED integration.

Sensors provided:
- Rotation: Current display rotation (0°, 90°, 180°, 270°)
- Brightness: Current brightness as percentage (0-100%)
- Active Plugin: Currently active plugin name
- Status: Device status (NONE, WSBINARY, UPDATE, LOADING)
- Schedule Count: Number of scheduled items
- WiFi Signal: WiFi signal strength (dBm) - Diagnostic
- Uptime: Device uptime in seconds - Diagnostic
- Free Memory: Free heap memory in bytes - Diagnostic
- IP Address: Device IP address - Diagnostic
- MAC Address: Device MAC address - Diagnostic

Classes:
    IkeaObegransadRotationSensor: Sensor for display rotation.
    IkeaObegransadBrightnessSensor: Sensor for brightness percentage.
    IkeaObegransadActivePluginSensor: Sensor for active plugin name.
    IkeaObegransadStatusSensor: Sensor for device status.
    IkeaObegransadScheduleCountSensor: Sensor for schedule item count.
    IkeaObegransadWifiSignalSensor: Diagnostic sensor for WiFi signal strength.
    IkeaObegransadUptimeSensor: Diagnostic sensor for device uptime.
    IkeaObegransadFreeMemorySensor: Diagnostic sensor for free memory.
    IkeaObegransadIpAddressSensor: Diagnostic sensor for IP address.
    IkeaObegransadMacAddressSensor: Diagnostic sensor for MAC address.

Functions:
    async_setup_entry: Sets up the sensor platform.
"""

import logging
from collections.abc import Callable

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_HOST, DOMAIN, VERSION

_LOGGER: logging.Logger = logging.getLogger(__package__)

# Rotation mapping
ROTATION_MAP = {0: "0°", 1: "90°", 2: "180°", 3: "270°"}


class IkeaObegransadRotationSensor(CoordinatorEntity, SensorEntity):
    """Sensor for display rotation."""

    _attr_has_entity_name = True
    _attr_icon = "mdi:screen-rotation"
    _attr_translation_key = "rotation"

    def __init__(self, coordinator: CoordinatorEntity, entry: ConfigEntry) -> None:
        """Initialize the rotation sensor."""
        super().__init__(coordinator)
        self.entry = entry
        self._attr_unique_id = f"{entry.entry_id}_rotation"
        self._attr_name = "Rotation"

    @property
    def native_value(self) -> str:
        """Return the current rotation."""
        return ROTATION_MAP.get(self.coordinator.rotation, "Unknown")

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
        _LOGGER.debug("Rotation sensor update: %s", self.coordinator.rotation)
        self.async_write_ha_state()


class IkeaObegransadBrightnessSensor(CoordinatorEntity, SensorEntity):
    """Sensor for brightness percentage."""

    _attr_has_entity_name = True
    _attr_icon = "mdi:brightness-6"
    _attr_translation_key = "brightness"
    _attr_native_unit_of_measurement = "%"
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator: CoordinatorEntity, entry: ConfigEntry) -> None:
        """Initialize the brightness sensor."""
        super().__init__(coordinator)
        self.entry = entry
        self._attr_unique_id = f"{entry.entry_id}_brightness"
        self._attr_name = "Brightness"

    @property
    def native_value(self) -> int:
        """Return brightness as percentage (0-100)."""
        return round(self.coordinator.brightness * 100 / 255)

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
        _LOGGER.debug("Brightness sensor update: %s", self.coordinator.brightness)
        self.async_write_ha_state()


class IkeaObegransadActivePluginSensor(CoordinatorEntity, SensorEntity):
    """Sensor for active plugin name."""

    _attr_has_entity_name = True
    _attr_icon = "mdi:puzzle"
    _attr_translation_key = "active_plugin"

    def __init__(self, coordinator: CoordinatorEntity, entry: ConfigEntry) -> None:
        """Initialize the active plugin sensor."""
        super().__init__(coordinator)
        self.entry = entry
        self._attr_unique_id = f"{entry.entry_id}_active_plugin"
        self._attr_name = "Active Plugin"

    @property
    def native_value(self) -> str | None:
        """Return the active plugin name."""
        return self.coordinator.active_effect_name

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
            "Active plugin sensor update: %s", self.coordinator.active_effect_name
        )
        self.async_write_ha_state()


class IkeaObegransadStatusSensor(CoordinatorEntity, SensorEntity):
    """Sensor for device status."""

    _attr_has_entity_name = True
    _attr_icon = "mdi:information"
    _attr_translation_key = "status"

    def __init__(self, coordinator: CoordinatorEntity, entry: ConfigEntry) -> None:
        """Initialize the status sensor."""
        super().__init__(coordinator)
        self.entry = entry
        self._attr_unique_id = f"{entry.entry_id}_status"
        self._attr_name = "Status"

    @property
    def native_value(self) -> str:
        """Return the device status."""
        return self.coordinator.status

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
        _LOGGER.debug("Status sensor update: %s", self.coordinator.status)
        self.async_write_ha_state()


class IkeaObegransadScheduleCountSensor(CoordinatorEntity, SensorEntity):
    """Sensor for schedule item count."""

    _attr_has_entity_name = True
    _attr_icon = "mdi:calendar-clock"
    _attr_translation_key = "schedule_count"
    _attr_native_unit_of_measurement = "items"
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator: CoordinatorEntity, entry: ConfigEntry) -> None:
        """Initialize the schedule count sensor."""
        super().__init__(coordinator)
        self.entry = entry
        self._attr_unique_id = f"{entry.entry_id}_schedule_count"
        self._attr_name = "Schedule Count"

    @property
    def native_value(self) -> int:
        """Return the number of scheduled items."""
        return len(self.coordinator.schedule)

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
        _LOGGER.debug("Schedule count sensor update: %s", len(self.coordinator.schedule))
        self.async_write_ha_state()


# Diagnostic Sensors


class IkeaObegransadWifiSignalSensor(CoordinatorEntity, SensorEntity):
    """Diagnostic sensor for WiFi signal strength."""

    _attr_has_entity_name = True
    _attr_icon = "mdi:wifi"
    _attr_translation_key = "wifi_signal"
    _attr_device_class = SensorDeviceClass.SIGNAL_STRENGTH
    _attr_native_unit_of_measurement = "dBm"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, coordinator: CoordinatorEntity, entry: ConfigEntry) -> None:
        """Initialize the WiFi signal sensor."""
        super().__init__(coordinator)
        self.entry = entry
        self._attr_unique_id = f"{entry.entry_id}_wifi_signal"
        self._attr_name = "WiFi Signal"

    @property
    def native_value(self) -> int | None:
        """Return WiFi signal strength in dBm."""
        return self.coordinator.wifi_rssi

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
        _LOGGER.debug("WiFi signal sensor update: %s", self.coordinator.wifi_rssi)
        self.async_write_ha_state()


class IkeaObegransadUptimeSensor(CoordinatorEntity, SensorEntity):
    """Diagnostic sensor for device uptime."""

    _attr_has_entity_name = True
    _attr_icon = "mdi:clock-outline"
    _attr_translation_key = "uptime"
    _attr_device_class = SensorDeviceClass.DURATION
    _attr_native_unit_of_measurement = "s"
    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, coordinator: CoordinatorEntity, entry: ConfigEntry) -> None:
        """Initialize the uptime sensor."""
        super().__init__(coordinator)
        self.entry = entry
        self._attr_unique_id = f"{entry.entry_id}_uptime"
        self._attr_name = "Uptime"

    @property
    def native_value(self) -> int | None:
        """Return device uptime in seconds."""
        return self.coordinator.uptime

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
        _LOGGER.debug("Uptime sensor update: %s", self.coordinator.uptime)
        self.async_write_ha_state()


class IkeaObegransadFreeMemorySensor(CoordinatorEntity, SensorEntity):
    """Diagnostic sensor for free memory."""

    _attr_has_entity_name = True
    _attr_icon = "mdi:memory"
    _attr_translation_key = "free_memory"
    _attr_native_unit_of_measurement = "B"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, coordinator: CoordinatorEntity, entry: ConfigEntry) -> None:
        """Initialize the free memory sensor."""
        super().__init__(coordinator)
        self.entry = entry
        self._attr_unique_id = f"{entry.entry_id}_free_memory"
        self._attr_name = "Free Memory"

    @property
    def native_value(self) -> int | None:
        """Return free memory in bytes."""
        return self.coordinator.free_memory

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
        _LOGGER.debug("Free memory sensor update: %s", self.coordinator.free_memory)
        self.async_write_ha_state()


class IkeaObegransadIpAddressSensor(CoordinatorEntity, SensorEntity):
    """Diagnostic sensor for device IP address."""

    _attr_has_entity_name = True
    _attr_icon = "mdi:ip-network"
    _attr_translation_key = "ip_address"
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, coordinator: CoordinatorEntity, entry: ConfigEntry) -> None:
        """Initialize the IP address sensor."""
        super().__init__(coordinator)
        self.entry = entry
        self._attr_unique_id = f"{entry.entry_id}_ip_address"
        self._attr_name = "IP Address"

    @property
    def native_value(self) -> str | None:
        """Return device IP address."""
        return self.coordinator.ip_address

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
        _LOGGER.debug("IP address sensor update: %s", self.coordinator.ip_address)
        self.async_write_ha_state()


class IkeaObegransadMacAddressSensor(CoordinatorEntity, SensorEntity):
    """Diagnostic sensor for device MAC address."""

    _attr_has_entity_name = True
    _attr_icon = "mdi:network"
    _attr_translation_key = "mac_address"
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, coordinator: CoordinatorEntity, entry: ConfigEntry) -> None:
        """Initialize the MAC address sensor."""
        super().__init__(coordinator)
        self.entry = entry
        self._attr_unique_id = f"{entry.entry_id}_mac_address"
        self._attr_name = "MAC Address"

    @property
    def native_value(self) -> str | None:
        """Return device MAC address."""
        return self.coordinator.mac_address

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
        _LOGGER.debug("MAC address sensor update: %s", self.coordinator.mac_address)
        self.async_write_ha_state()


class IkeaObegransadWeatherLocationSensor(CoordinatorEntity, SensorEntity):
    """Sensor for weather location configuration."""

    _attr_has_entity_name = True
    _attr_icon = "mdi:weather-cloudy"
    _attr_translation_key = "weather_location"

    def __init__(self, coordinator: CoordinatorEntity, entry: ConfigEntry) -> None:
        """Initialize the weather location sensor."""
        super().__init__(coordinator)
        self.entry = entry
        self._attr_unique_id = f"{entry.entry_id}_weather_location"
        self._attr_name = "Weather Location"

    @property
    def native_value(self) -> str | None:
        """Return the configured weather location."""
        location = self.coordinator.weather_location
        return location if location else None

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
        _LOGGER.debug("Weather location sensor update: %s", self.coordinator.weather_location)
        self.async_write_ha_state()


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: Callable
) -> None:
    """Set up the sensor platform for IKEA OBEGRÄNSAD LED."""
    _LOGGER.debug("Setting up sensor platform for IKEA OBEGRÄNSAD LED.")
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [
            IkeaObegransadRotationSensor(coordinator, entry),
            IkeaObegransadBrightnessSensor(coordinator, entry),
            IkeaObegransadActivePluginSensor(coordinator, entry),
            IkeaObegransadStatusSensor(coordinator, entry),
            IkeaObegransadScheduleCountSensor(coordinator, entry),
            IkeaObegransadWeatherLocationSensor(coordinator, entry),
            IkeaObegransadWifiSignalSensor(coordinator, entry),
            IkeaObegransadUptimeSensor(coordinator, entry),
            IkeaObegransadFreeMemorySensor(coordinator, entry),
            IkeaObegransadIpAddressSensor(coordinator, entry),
            IkeaObegransadMacAddressSensor(coordinator, entry),
        ]
    )
    _LOGGER.info("Successfully set up sensor platform for IKEA OBEGRÄNSAD LED.")
