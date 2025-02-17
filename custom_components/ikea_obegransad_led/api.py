"""API Client to interact with IKEA OBEGRÄNSAD LED."""

import logging

import aiohttp

TIMEOUT = 10

_LOGGER: logging.Logger = logging.getLogger(__package__)

HEADERS = {"Content-type": "application/json; charset=UTF-8"}


class IkeaObegransadLedApiClient:
    """API client to control the LED lamp via REST."""

    def __init__(self, session, host):
        """Initializes the connection with the device host."""
        _LOGGER.debug(
            "Initializing API client for IKEA OBEGRÄNSAD LED."
        )  # Log client init
        self.session = session
        self.host = host
        self.base_url = f"http://{host}/api"  # Use configured host

    async def _request(self, method, endpoint, params=None):
        """Performs a generic HTTP request."""
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
                if response.status == 200:
                    try:
                        json_data = await response.json()
                        _LOGGER.debug(
                            "Successfully parsed JSON response: %s", json_data
                        )  # Log JSON data
                        return json_data
                    except (
                        aiohttp.ContentTypeError
                    ) as e:  # Handle potential JSON decode errors
                        _LOGGER.error("Invalid JSON response from %s: %s", url, e)
                        return None
                else:
                    text = await response.text()  # Get error text
                    _LOGGER.error(
                        "API Error %s from %s: %s", response.status, url, text
                    )  # Log error details
                    return None
        except aiohttp.ClientError as err:
            _LOGGER.error("API connection error: %s", err)  # Log connection errors
            return None  # Important: Return None on error

    async def get_info(self):
        """Retrieves information about the device."""
        return await self._request("GET", "info")

    async def is_on(self):
        """Retrieves information about the device."""
        return self.get_brightness > 0

    async def turn_on(self):
        """Turns on the device."""
        return await self.set_brightness(255)

    async def turn_off(self):
        """Turns off the device."""
        return await self.set_brightness(0)

    async def set_plugin(self, plugin_id):
        """Sets an active plugin by ID."""
        return await self._request("PATCH", "plugin", {"id": plugin_id})

    async def get_plugins(self):
        """Retrieves available plugins."""
        return await self.get_info().data.get("plugins")

    async def get_active_plugin(self):
        """Retrieves the currently active plugin."""
        return await self.get_info().data.get("plugin")

    async def set_brightness(self, value):
        """Sets the LED display brightness."""
        return await self._request("PATCH", "brightness", {"value": value})

    async def get_brightness(self):
        """Retrieves the LED display brightness."""
        return await self.get_info().data.get("brightness")

    async def get_display_data(self):
        """Retrieves the current LED display data."""
        return await self._request("GET", "data")

    async def send_message(
        self, text=None, graph=None, repeat=1, delay=50, miny=None, maxy=None, id=None
    ):
        """Sends a message to the display."""
        params = {
            "text": text,
            "repeat": repeat,
            "delay": delay,
        }
        if graph is not None:
            params["graph"] = ",".join(map(str, graph))
        if miny is not None:
            params["miny"] = miny
        if maxy is not None:
            params["maxy"] = maxy
        if id is not None:
            params["id"] = id
        return await self._request("GET", "message", params=params)

    async def remove_message(self, message_id):
        """Removes a message from the LED display."""
        return await self._request("GET", "removemessage", {"id": message_id})
