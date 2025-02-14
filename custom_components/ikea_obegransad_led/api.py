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
        self.session = session
        self.host = host
        self.base_url = f"http://{host}/api"  # Usa l'host configurato

    async def _request(self, method, endpoint, params=None):
        """Effettua una richiesta HTTP generica."""
        url = f"{self.base_url}/{endpoint}"
        try:
            async with self.session.request(method, url, params=params) as response:
                if response.status == 200:
                    return await response.json()
                _LOGGER.error("Errore API %s: %s", url, response.status)
        except aiohttp.ClientError as err:
            _LOGGER.error("Errore di connessione API: %s", err)
        return None

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

    async def send_message(self, text=None, graph=None, repeat=1, delay=50):
        """Invia un messaggio al display LED."""
        params = {"text": text, "repeat": repeat, "delay": delay}
        if graph:
            params["graph"] = ",".join(map(str, graph))
        return await self._request("GET", "message", params)

    async def remove_message(self, message_id):
        """Rimuove un messaggio dal display LED."""
        return await self._request("GET", "removemessage", {"id": message_id})
