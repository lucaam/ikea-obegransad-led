"""
Camera platform for IKEA OBEGRÄNSAD LED.

This module provides a camera entity for the IKEA OBEGRÄNSAD LED integration.

The camera entity displays a live preview of the 16x16 LED matrix display.
It retrieves the raw pixel data from the device and converts it to a PNG image.

Classes:
    IkeaObegransadScreenCamera: Camera entity for LED matrix preview.

Functions:
    async_setup_entry: Sets up the camera platform.
"""

import logging
from collections.abc import Callable
from io import BytesIO

from homeassistant.components.camera import Camera, CameraEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_HOST, DOMAIN, VERSION

_LOGGER: logging.Logger = logging.getLogger(__package__)

try:
    from PIL import Image
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False


class IkeaObegransadScreenCamera(CoordinatorEntity, Camera):
    """Camera entity for LED matrix preview."""

    _attr_has_entity_name = True
    _attr_icon = "mdi:camera"
    _attr_translation_key = "screen"
    _attr_supported_features = CameraEntityFeature.ON_OFF

    def __init__(self, coordinator: CoordinatorEntity, entry: ConfigEntry) -> None:
        """Initialize the camera entity."""
        Camera.__init__(self)
        CoordinatorEntity.__init__(self, coordinator)
        self.entry = entry
        self._attr_unique_id = f"{entry.entry_id}_screen_camera"
        self._attr_name = "Screen"
        self._frame_interval = 1.0  # Refresh every second

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

    async def async_camera_image(
        self, width: int | None = None, height: int | None = None
    ) -> bytes | None:
        """Return the current camera image as JPEG."""
        if not PILLOW_AVAILABLE:
            _LOGGER.error("PIL/Pillow not available for camera image processing")
            return None

        try:
            # Get raw display data (256 bytes for 16x16 matrix)
            data = await self.coordinator.client.get_display_data()
            if not data:
                _LOGGER.warning("Invalid display data: empty response")
                return None
            if len(data) != 256:
                _LOGGER.warning(
                    "Invalid display data: expected 256 bytes, got %s. "
                    "Normalizing to 256 bytes for preview.",
                    len(data),
                )
                if len(data) < 256:
                    data = data.ljust(256, b"\x00")
                else:
                    data = data[:256]

            # Convert 256 bytes to 16x16 grayscale image
            # Each byte represents the brightness of one pixel (0-255)
            image_array = [data[i] for i in range(256)]
            img = Image.new("L", (16, 16))
            img.putdata(image_array)

            # Scale up for better visibility (16x16 -> 256x256)
            scale = 16
            img = img.resize((16 * scale, 16 * scale), Image.NEAREST)

            # Convert to JPEG
            output = BytesIO()
            img.save(output, format="JPEG", quality=95)
            return output.getvalue()

        except Exception as e:
            _LOGGER.exception("Error generating camera image: %s", e)
            return None

    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        _LOGGER.debug("Screen camera update triggered")
        self.async_write_ha_state()


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: Callable
) -> None:
    """Set up the camera platform for IKEA OBEGRÄNSAD LED."""
    if not PILLOW_AVAILABLE:
        _LOGGER.warning(
            "PIL/Pillow library not found. Camera entity will not work. "
            "Install with: pip install Pillow"
        )

    _LOGGER.debug("Setting up camera platform for IKEA OBEGRÄNSAD LED.")
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([IkeaObegransadScreenCamera(coordinator, entry)])
    _LOGGER.info("Successfully set up camera platform for IKEA OBEGRÄNSAD LED.")
