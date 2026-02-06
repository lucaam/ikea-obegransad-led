"""
Notify platform for IKEA OBEGRÄNSAD LED.

This module provides a notify service for the IKEA OBEGRÄNSAD LED integration.

The notify service allows sending messages to the LED display using the standard
Home Assistant notification framework.

Service: notify.ikea_obegransad_led

Message format:
{
  "message": "Text to display",
  "title": "Optional title (not used)",
  "data": {
    "repeat": 1,  # Number of times to repeat (default: 1)
    "delay": 50,  # Scroll delay in ms (default: 50)
    "message_id": "unique_id",  # Optional message ID
    "graph": "1,2,3,4,5",  # Optional graph data as comma-separated values
    "miny": 0,  # Optional graph Y-axis minimum
    "maxy": 100  # Optional graph Y-axis maximum
  }
}

Classes:
    IkeaObegransadNotifyService: Notify service for sending messages to the display.

Functions:
    async_get_service: Returns the notify service instance.
"""

import logging
from typing import Any

from homeassistant.components.notify import (
    ATTR_DATA,
    BaseNotificationService,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN

_LOGGER: logging.Logger = logging.getLogger(__package__)


class IkeaObegransadNotifyService(BaseNotificationService):
    """Notify service for IKEA OBEGRÄNSAD LED."""

    def __init__(self, coordinator: Any) -> None:
        """Initialize the notify service."""
        self.coordinator = coordinator
        _LOGGER.debug("IkeaObegransadNotifyService initialized")

    async def async_send_message(self, message: str = "", **kwargs: Any) -> None:
        """
        Send a message to the IKEA OBEGRÄNSAD LED display.

        Args:
            message: The text message to display
            **kwargs: Additional parameters including:
                - data: Dictionary containing optional parameters:
                    - repeat: Number of repeats (default: 1)
                    - delay: Scroll delay in ms (default: 50)
                    - message_id: Optional message ID
                    - graph: Graph data as comma-separated string
                    - miny: Graph Y-axis minimum
                    - maxy: Graph Y-axis maximum

        """
        if not message:
            _LOGGER.error("No message provided to notify service")
            return

        data = kwargs.get(ATTR_DATA, {})
        repeat = data.get("repeat", 1)
        delay = data.get("delay", 50)
        message_id = data.get("message_id")
        graph_str = data.get("graph")
        miny = data.get("miny")
        maxy = data.get("maxy")

        # Parse graph string to list if provided
        graph = None
        if graph_str:
            try:
                if isinstance(graph_str, str):
                    graph = [int(x.strip()) for x in graph_str.split(",")]
                elif isinstance(graph_str, list):
                    graph = [int(x) for x in graph_str]
            except (ValueError, TypeError):
                _LOGGER.error("Invalid graph format: %s", graph_str)
                graph = None

        try:
            # Switch to DDP plugin for displaying messages
            from .const import CONF_DEFAULT_MESSAGE_BACKGROUND_EFFECT

            await self.coordinator.client.set_plugin_by_name(
                CONF_DEFAULT_MESSAGE_BACKGROUND_EFFECT
            )

            # Send the message
            await self.coordinator.client.send_message(
                text=message,
                repeat=repeat,
                delay=delay,
                graph=graph,
                miny=miny,
                maxy=maxy,
                message_id=message_id,
            )
            _LOGGER.info(
                "Message sent to IKEA OBEGRÄNSAD LED: %s (repeat: %d, delay: %d)",
                message,
                repeat,
                delay,
            )
        except Exception as e:
            _LOGGER.exception("Failed to send message to IKEA OBEGRÄNSAD LED: %s", e)


async def async_get_service(
    hass: HomeAssistant,
    service_name: str,
    discovery_info: ConfigType | None = None,
) -> BaseNotificationService | None:
    """Return the notify service."""
    _LOGGER.debug("Setting up IKEA OBEGRÄNSAD LED notify service")

    if DOMAIN not in hass.data or not hass.data[DOMAIN]:
        _LOGGER.error("IKEA OBEGRÄNSAD LED integration not configured")
        return None

    # Get the first (and usually only) coordinator
    coordinators = list(hass.data[DOMAIN].values())
    if not coordinators:
        _LOGGER.error("No coordinators found")
        return None

    coordinator = coordinators[0]
    return IkeaObegransadNotifyService(coordinator)
