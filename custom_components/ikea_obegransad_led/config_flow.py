"""
The module contains the configuration flow for the ikea_obegransad_led integration.

Classes:
    IkeaObegransadLedFlowHandler: Handles the configuration flow for the
    ikea_obegransad_led integration.

Functions:
    async_step_user: Handles a flow initialized by the user.
    _show_config_form: Shows the configuration form to edit location data.
    _test_host: Tests if the provided host is valid.

Constants:
    DEFAULT_HOST: The default host for the ikea_obegransad_led integration.
"""

import logging
from collections.abc import Coroutine

import aiohttp
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from .api import IkeaObegransadLedApiClient
from .const import CONF_HOST, DOMAIN

_LOGGER = logging.getLogger(__name__)

DEFAULT_HOST = "ikealedmatrix.home.network"


class IkeaObegransadLedFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for ikea_obegransad_led."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH

    def __init__(self) -> None:
        """Initialize."""
        self._errors = {}

    async def async_step_user(self, user_input: dict | None) -> Coroutine:
        """
        Handle a flow initialized by the user.

        This method is called when the user initiates the configuration flow.
        It validates the user input and creates an entry if the input is valid.
        If the input is invalid, it shows the configuration form again with errors.

        Args:
            user_input (dict, optional): The user input containing configuration data.
            Defaults to None.

        Returns:
            Coroutine: A coroutine that resolves to the next step in the
            configuration flow.

        """
        self._errors = {}

        if user_input is not None:
            host = user_input[CONF_HOST]
            valid = await self._test_host(host)
            if valid:
                return self.async_create_entry(title=host, data=user_input)
            self._errors["base"] = "cannot_connect"

            return await self._show_config_form(user_input)

        return await self._show_config_form(user_input)

    async def _show_config_form(
        self,
        user_input: dict | None,  # noqa: ARG002
    ) -> Coroutine:
        """
        Show the configuration form to edit location data.

        Returns:
            Coroutine: A coroutine that shows the configuration form.

        """
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {vol.Required(CONF_HOST, default=DEFAULT_HOST): str}
            ),
            errors=self._errors,
        )

    async def _test_host(self, host: str) -> bool:
        """
        Test the connection to the given host.

        This method attempts to establish a connection to the specified host
        and checks if a valid response is received.

        Args:
            host (str): The host address to test.

        Returns:
            bool: True if the host is valid and a valid response is received,
            False otherwise.

        Raises:
            aiohttp.ClientError: If there is a connection error.
            Exception: If an unexpected error occurs.

        """
        try:
            _LOGGER.debug("Testing connection to %s", host)
            session = async_create_clientsession(self.hass)
            client = IkeaObegransadLedApiClient(session, host)
            response = await client.get_info()

            if response:
                _LOGGER.debug("Received valid response: %s", response)
                return True
            _LOGGER.warning("Invalid response received: %s", response)

        except aiohttp.ClientError:
            _LOGGER.exception("Connection error")
            return False
        except Exception:
            _LOGGER.exception("Unexpected error")
            return False
