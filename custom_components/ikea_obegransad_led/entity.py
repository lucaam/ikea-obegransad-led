"""Entity for IKEA OBEGRÄNSAD Led integration."""

import logging

from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import slugify

from .const import DEFAULT_NAME, DOMAIN, VERSION

_LOGGER: logging.Logger = logging.getLogger(__package__)


class IkeaObegransadLedEntity(CoordinatorEntity, Entity):
    """Base class for IKEA OBEGRÄNSAD Led entities."""

    def __init__(self, coordinator, entry):
        """Initialize the entity with the data coordinator."""
        _LOGGER.debug(
            "Initializing entity for IKEA OBEGRÄNSAD Led."
        )  # Log entity initialization
        super().__init__(coordinator)
        self.entry = entry
        self._name = DEFAULT_NAME

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
    def extra_state_attributes(self):
        """Return the state attributes of the entity."""
        if self.coordinator.data:
            _LOGGER.debug(
                "Returning state attributes: %s", self.coordinator.data
            )  # Log state attributes
            return {
                "id": str(self.coordinator.data.get("id")),
                # Add other attributes as needed
            }
        return {}
