"""API Client to interact with IKEA OBEGRÄNSAD Led."""

import logging

import aiohttp

TIMEOUT = 10

_LOGGER: logging.Logger = logging.getLogger(__package__)

HEADERS = {"Content-type": "application/json; charset=UTF-8"}


class IkeaObegransadLedApiClient:
    """API client per controllare la lampada LED via REST."""

    def __init__(self, session, host):
        """Inizializza la connessione con l'host del dispositivo."""
        _LOGGER.debug(
            "Initializing API client for IKEA OBEGRÄNSAD Led."
        )  # Log client init
        self.session = session
        self.host = host
        self.base_url = f"http://{host}/api"  # Usa l'host configurato

    async def _request(self, method, endpoint, params=None):
        """Effettua una richiesta HTTP generica."""
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
        """Recupera informazioni sul dispositivo."""
        return await self._request("GET", "info")

    async def set_plugin(self, plugin_id):
        """Imposta un plugin attivo tramite ID."""
        return await self._request("PATCH", "plugin", {"id": plugin_id})

    async def set_brightness(self, value):
        """Imposta la luminosità del display LED."""
        return await self._request("PATCH", "brightness", {"value": value})

    async def get_display_data(self):
        """Recupera i dati attuali del display LED."""
        return await self._request("GET", "data")

    async def send_message(
        self, text=None, graph=None, repeat=1, delay=50, miny=None, maxy=None, id=None
    ):
        """Send message to display."""
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
        """Rimuove un messaggio dal display LED."""
        return await self._request("GET", "removemessage", {"id": message_id})
