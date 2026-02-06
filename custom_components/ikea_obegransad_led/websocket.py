"""
WebSocket client for real-time communication with IKEA OBEGRÄNSAD LED device.

This module provides WebSocket support for features that require real-time
bidirectional communication with the device, such as:
- Display rotation
- Plugin persistence
- Real-time display data updates
- Live drawing/binary data streaming

The WebSocket connection complements the REST API by enabling instant updates
and more efficient communication for certain operations.

Classes:
    IkeaObegransadWebSocket: WebSocket client for the device.

Note:
    This is currently a stub implementation. Full WebSocket support requires
    maintaining a persistent connection and handling reconnection logic.
    The firmware websocket endpoint is at ws://{host}/ws
"""

import asyncio
import logging
from typing import Any, Callable

import aiohttp

_LOGGER: logging.Logger = logging.getLogger(__package__)


class IkeaObegransadWebSocket:
    """WebSocket client for real-time updates and control."""

    def __init__(self, host: str, session: aiohttp.ClientSession) -> None:
        """
        Initialize the WebSocket client.

        Args:
            host (str): The device hostname or IP address.
            session (aiohttp.ClientSession): The aiohttp client session.

        """
        self.host = host
        self.session = session
        self.ws_url = f"ws://{host}/ws"
        self._ws: aiohttp.ClientWebSocketResponse | None = None
        self._connected = False
        self._closing = False
        self._callbacks: list[Callable] = []
        self._max_backoff = 300
        _LOGGER.debug("WebSocket client initialized for host: %s", host)

    async def connect(self) -> bool:
        """
        Connect to the device WebSocket.

        Returns:
            bool: True if connection successful, False otherwise.

        """
        if self._closing:
            _LOGGER.debug("WebSocket connect skipped: closing requested")
            return False

        if self._connected and self._ws and not self._ws.closed:
            return True

        try:
            _LOGGER.debug("Connecting to WebSocket at %s", self.ws_url)
            self._ws = await self.session.ws_connect(self.ws_url)
            self._connected = True
            _LOGGER.info("WebSocket connected successfully")
            return True
        except (aiohttp.ClientError, asyncio.TimeoutError) as err:
            _LOGGER.error("Failed to connect to WebSocket: %s", err)
            self._connected = False
            return False

    async def disconnect(self) -> None:
        """Disconnect from the WebSocket."""
        self._closing = True
        if self._ws and not self._ws.closed:
            await self._ws.close()
            _LOGGER.debug("WebSocket disconnected")
        self._connected = False

    @property
    def connected(self) -> bool:
        """Return whether the WebSocket is connected."""
        return self._connected and self._ws is not None and not self._ws.closed

    async def send_json(self, data: dict[str, Any]) -> bool:
        """
        Send JSON data to the device.

        Args:
            data (dict): The data to send.

        Returns:
            bool: True if sent successfully, False otherwise.

        """
        if not self.connected:
            _LOGGER.warning("WebSocket not connected, attempting to reconnect")
            if not await self.connect():
                return False

        try:
            await self._ws.send_json(data)
            _LOGGER.debug("Sent WebSocket message: %s", data)
            return True
        except (aiohttp.ClientError, RuntimeError) as err:
            _LOGGER.error("Failed to send WebSocket message: %s", err)
            self._connected = False
            return False

    async def send_binary(self, data: bytes) -> bool:
        """
        Send binary data to the device.

        Used for sending raw display data when currentStatus is WSBINARY.

        Args:
            data (bytes): The binary data to send (should be 256 bytes for 16x16).

        Returns:
            bool: True if sent successfully, False otherwise.

        """
        if not self.connected:
            _LOGGER.warning("WebSocket not connected, attempting to reconnect")
            if not await self.connect():
                return False

        if len(data) != 256:
            _LOGGER.error(
                "Invalid binary data size: %d bytes (expected 256)", len(data)
            )
            return False

        try:
            await self._ws.send_bytes(data)
            _LOGGER.debug("Sent %d bytes of binary data", len(data))
            return True
        except (aiohttp.ClientError, RuntimeError) as err:
            _LOGGER.error("Failed to send binary data: %s", err)
            self._connected = False
            return False

    async def rotate_display(self, direction: str = "right") -> bool:
        """
        Send rotation command to the device.

        Args:
            direction (str): Rotation direction ('right' or 'left').

        Returns:
            bool: True if command sent successfully, False otherwise.

        """
        data = {"event": "rotate", "direction": direction}
        return await self.send_json(data)

    async def persist_plugin(self) -> bool:
        """
        Send command to persist the current plugin.

        Returns:
            bool: True if command sent successfully, False otherwise.

        """
        data = {"event": "persist-plugin"}
        return await self.send_json(data)

    async def set_plugin(self, plugin_id: int) -> bool:
        """
        Set active plugin via WebSocket.

        Args:
            plugin_id (int): The plugin ID to activate.

        Returns:
            bool: True if command sent successfully, False otherwise.

        """
        data = {"event": "plugin", "plugin": plugin_id}
        return await self.send_json(data)

    async def set_brightness(self, brightness: int) -> bool:
        """
        Set brightness via WebSocket.

        Args:
            brightness (int): Brightness value (0-255).

        Returns:
            bool: True if command sent successfully, False otherwise.

        """
        data = {"event": "brightness", "brightness": brightness}
        return await self.send_json(data)

    async def request_info(self) -> bool:
        """
        Request device info update via WebSocket.

        Returns:
            bool: True if command sent successfully, False otherwise.

        """
        data = {"event": "info"}
        return await self.send_json(data)

    def add_callback(self, callback: Callable) -> None:
        """
        Add a callback to be called when WebSocket messages are received.

        Args:
            callback (Callable): The callback function.

        """
        self._callbacks.append(callback)

    def remove_callback(self, callback: Callable) -> None:
        """
        Remove a callback.

        Args:
            callback (Callable): The callback function to remove.

        """
        if callback in self._callbacks:
            self._callbacks.remove(callback)

    async def listen(self) -> None:
        """
        Listen for incoming WebSocket messages.

        This is a long-running coroutine that should be run as a task.
        It will continuously listen for messages and call registered callbacks.
        """
        if not self.connected:
            _LOGGER.debug("WebSocket listen called while disconnected")
            return

        try:
            async for msg in self._ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    try:
                        data = msg.json()
                        _LOGGER.debug("Received WebSocket message: %s", data)
                        for callback in self._callbacks:
                            try:
                                await callback(data)
                            except Exception as err:
                                _LOGGER.exception(
                                    "Error in WebSocket callback: %s", err
                                )
                    except ValueError:
                        _LOGGER.error("Failed to parse WebSocket message as JSON")
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    _LOGGER.error("WebSocket error: %s", self._ws.exception())
                    break
                elif msg.type in (
                    aiohttp.WSMsgType.CLOSED,
                    aiohttp.WSMsgType.CLOSING,
                ):
                    _LOGGER.info("WebSocket connection closing")
                    break
        except Exception as err:
            _LOGGER.exception("Error in WebSocket listener: %s", err)
        finally:
            self._connected = False
            _LOGGER.debug("WebSocket listener stopped")

    async def listen_forever(self) -> None:
        """
        Listen for incoming WebSocket messages with automatic reconnection.

        Uses exponential backoff with a max delay of 5 minutes.
        """
        self._closing = False
        backoff = 1

        while not self._closing:
            connected = await self.connect()
            if not connected:
                await asyncio.sleep(backoff)
                backoff = min(self._max_backoff, backoff * 2)
                continue

            backoff = 1
            await self.listen()

            if not self._closing:
                await asyncio.sleep(backoff)
                backoff = min(self._max_backoff, backoff * 2)
