"""Binary sensor platform for IKEA OBEGRÄNSAD Led."""

from homeassistant.components.binary_sensor import BinarySensorEntity

from .const import BINARY_SENSOR
from .const import BINARY_SENSOR_DEVICE_CLASS
from .const import DEFAULT_NAME
from .const import DOMAIN
from .entity import IkeaObegransadLedEntity
import logging


_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup binary_sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices([IkeaObegransadLedBinarySensor(coordinator, entry)])


class IkeaObegransadLedBinarySensor(IkeaObegransadLedEntity, BinarySensorEntity):
    """ikea_obegransad_led binary_sensor class."""

    @property
    def name(self):
        """Return the name of the binary_sensor."""
        return f"{DEFAULT_NAME}_{BINARY_SENSOR}"

    @property
    def device_class(self):
        """Return the class of this binary_sensor."""
        return BINARY_SENSOR_DEVICE_CLASS

    @property
    def is_on(self):
        """Return true if the device is connected."""
        return self.coordinator.last_update_success
