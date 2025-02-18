"""
A module provides an API client to control the IKEA OBEGRÄNSAD LED lamp via REST.

Classes:
    IkeaObegransadLedApiClient: API client to interact with the LED lamp.

Constants:
    TIMEOUT (int): The timeout duration for HTTP requests.
    HEADERS (dict): The headers used for HTTP requests.

Functions:
    __init__(self, session, host): Initializes the connection with the device host.
    _request(self, method, endpoint, params=None): Performs a generic HTTP request.
    get_info(self): Retrieves information about the device.
    is_on(self): Checks if the light is on.
    turn_on(self): Turns on the device.
    turn_off(self): Turns off the device.
    set_plugin(self, plugin_id): Sets an active plugin by ID.
    get_plugins(self): Retrieves available plugins.
    get_active_plugin(self): Retrieves the currently active plugin.
    set_brightness(self, value): Sets the LED display brightness.
    get_brightness(self): Retrieves the LED display brightness.
    get_display_data(self): Retrieves the current LED display data.
    send_message(
        self, text=None, graph=None, repeat=1, delay=50, miny=None, maxy=None, id=None
    ): Sends a message to the display.
    remove_message(self, message_id: str): Removes a message from the LED display.
"""

import logging
from typing import Any

import aiohttp

TIMEOUT = 10
HTTP_OK = 200

_LOGGER: logging.Logger = logging.getLogger(__package__)

HEADERS = {"Content-type": "application/json; charset=UTF-8"}


class IkeaObegransadLedApiClient:
    """API client to control the LED lamp via REST."""

    def __init__(self, session: aiohttp.ClientSession, host: str) -> None:
        """Initialize the connection with the device host."""
        _LOGGER.debug(
            "Initializing API client for IKEA OBEGRÄNSAD LED with host: %s", host
        )  # Log client init
        self.session = session
        self.host = host
        self.base_url = f"http://{host}/api"  # Use configured host
        _LOGGER.debug("Base URL set to: %s", self.base_url)

    async def _request(
        self, method: str, endpoint: str, params: dict[str, Any] | None = None
    ) -> dict[str, Any] | None:
        """
        Perform a generic HTTP request.

        Args:
            method (str): The HTTP method to use for the request (e.g., 'GET', 'POST').
            endpoint (str): The API endpoint to send the request to.
            params (dict, optional): The parameters to include in the request.
                Defaults to None.

        Returns:
            dict or None: The JSON response from the API if the request is successful
                and the response is valid JSON.
                None if the request fails or the response is not valid JSON.

        Logs:
            - Request details including method, URL, and parameters.
            - Response status and URL.
            - JSON response data if successfully parsed.
            - Errors including invalid JSON responses, API errors, and connection
                errors.

        """
        url = f"{self.base_url}/{endpoint}"
        _LOGGER.debug(
            "Making %s request to %s with params: %s", method, url, params
        )  # Log request details
        try:
            async with self.session.request(
                method, url, params=params, timeout=TIMEOUT
            ) as response:  # Add timeout
                _LOGGER.debug(
                    "Received response with status: %s from %s", response.status, url
                )  # Log response status
                if response.status == HTTP_OK:
                    try:
                        json_data = await response.json()
                        _LOGGER.debug(
                            "Successfully parsed JSON response: %s", json_data
                        )  # Log JSON data
                        return json_data
                    except (
                        aiohttp.ContentTypeError
                    ):  # Handle potential JSON decode errors
                        _LOGGER.exception(
                            "Invalid JSON response from %s, %s", url, json_data
                        )
                        return None
                    else:
                        _LOGGER.exception(
                            "Invalid JSON response from %s, %s", url, json_data
                        )
                        return None
                else:
                    text = await response.text()  # Get error text
                    _LOGGER.error(
                        "API Error %s from %s: %s", response.status, url, text
                    )  # Log error details
                    return None
        except aiohttp.ClientError:
            _LOGGER.exception("API connection error")  # Log connection errors
            return None  # Important: Return None on error

    async def get_info(self) -> dict[str, Any] | None:
        """Retrieve information about the device."""
        _LOGGER.debug("Requesting device info from %s", self.base_url)
        info = await self._request("GET", "info")
        _LOGGER.debug("Device info received: %s", info)
        return info

    async def is_on(self) -> bool:
        """Check if the light is on."""
        brightness = (
            await self.get_brightness()
        )  # Ensure brightness is fetched correctly
        _LOGGER.debug("Brightness value for is_on check: %s", brightness)
        return brightness > 0

    async def turn_on(self) -> dict[str, Any] | None:
        """Turn on the device."""
        _LOGGER.debug("Turning on the device by setting brightness to 255")
        return await self.set_brightness(255)

    async def turn_off(self) -> dict[str, Any] | None:
        """Turn off the device."""
        _LOGGER.debug("Turning off the device by setting brightness to 0")
        return await self.set_brightness(0)

    async def set_plugin(self, plugin_id: str) -> dict[str, Any] | None:
        """Set an active plugin by ID."""
        _LOGGER.debug("Setting plugin with ID: %s", plugin_id)
        response = await self._request("PATCH", "plugin", {"id": plugin_id})
        _LOGGER.debug("Plugin set response: %s", response)
        return response

    async def get_plugins(self) -> list[dict[str, Any]]:
        """Retrieve available plugins."""
        _LOGGER.debug("Requesting available plugins.")
        info = await self.get_info()  # Use get_info correctly
        plugins = info.get("plugins", [])
        _LOGGER.debug("Available plugins: %s", plugins)
        return plugins

    async def get_active_plugin(self) -> dict[str, Any] | None:
        """Retrieve the currently active plugin."""
        _LOGGER.debug("Requesting active plugin.")
        info = await self.get_info()  # Use get_info correctly
        active_plugin = info.get("plugin")
        _LOGGER.debug("Active plugin: %s", active_plugin)
        return active_plugin

    async def set_brightness(self, value: int) -> dict[str, Any] | None:
        """Set the LED display brightness."""
        _LOGGER.debug("Setting brightness to: %s", value)
        return await self._request("PATCH", "brightness", {"value": value})

    async def get_brightness(self) -> int:
        """Retrieve the LED display brightness."""
        _LOGGER.debug("Requesting brightness value from the device.")
        info = await self.get_info()  # Use get_info correctly
        brightness = info.get("brightness", 0)
        _LOGGER.debug("Brightness retrieved: %s", brightness)
        return brightness

    async def get_display_data(self) -> dict[str, Any] | None:
        """Retrieve the current LED display data."""
        _LOGGER.debug("Requesting display data from the device.")
        return await self._request("GET", "data")

    async def send_message(  # noqa: PLR0913
        self,
        text: str | None = None,
        graph: list[int] | None = None,
        repeat: int = 1,
        delay: int = 50,
        miny: int | None = None,
        maxy: int | None = None,
        message_id: str | None = None,
    ) -> dict[str, Any] | None:
        """Send a message to the display."""
        params = {"text": text, "repeat": repeat, "delay": delay}
        if message_id is not None:
            params["id"] = message_id
        if graph is not None:
            params["graph"] = ",".join(map(str, graph))
        if miny is not None:
            params["miny"] = miny
        if maxy is not None:
            params["maxy"] = maxy
        if message_id is not None:
            params["id"] = message_id
        _LOGGER.debug("Sending message with params: %s", params)
        return await self._request("GET", "message", params=params)

    async def remove_message(self, message_id: str) -> dict[str, Any] | None:
        """
        Remove a message from the LED display.

        Args:
            message_id (str): The ID of the message to be removed.

        Returns:
            dict: The response from the LED display after attempting
            to remove the message.

        """
        _LOGGER.debug("Removing message with ID: %s", message_id)
        return await self._request("GET", "removemessage", {"id": message_id})
