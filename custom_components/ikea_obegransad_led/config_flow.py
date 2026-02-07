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
from .const import (
    CONF_DEFAULT_MESSAGE_BACKGROUND_EFFECT,
    CONF_HOST,
    CONF_WEATHER_LOCATION,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

DEFAULT_HOST = "ikealedmatrix.home.network"


class IkeaObegransadLedFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for ikea_obegransad_led."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize."""
        self._errors = {}
        self._host = None

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
            host = user_input[CONF_HOST].strip()
            effect = user_input[CONF_DEFAULT_MESSAGE_BACKGROUND_EFFECT]

            # Check if already configured
            await self.async_set_unique_id(host.lower())
            self._abort_if_unique_id_configured()

            valid_host = await self._test_host(host)
            if valid_host:
                valid_effect = await self._verify_effect_exists(host, effect)
                if valid_effect:
                    return self.async_create_entry(
                        title=f"IKEA LED Matrix ({host})",
                        data=user_input,
                    )
                self._errors["base"] = "effect_does_not_exist"
            else:
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
                {
                    vol.Required(CONF_HOST, default=DEFAULT_HOST): str,
                    vol.Required(
                        CONF_DEFAULT_MESSAGE_BACKGROUND_EFFECT,
                        default=CONF_DEFAULT_MESSAGE_BACKGROUND_EFFECT,
                    ): str,
                    vol.Optional(CONF_WEATHER_LOCATION, default=""): str,
                },
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
            return False  # noqa: TRY300

        except aiohttp.ClientError:
            _LOGGER.exception("Connection error")
            return False
        except Exception:
            _LOGGER.exception("Unexpected error")
            return False

    async def _verify_effect_exists(self, host: str, effect: str) -> bool:
        try:
            _LOGGER.debug("Testing connection to %s", host)
            session = async_create_clientsession(self.hass)
            client = IkeaObegransadLedApiClient(session, host)
            response = await client.get_plugin_id_by_name(effect)

            if response:
                _LOGGER.debug("Effect name %s exists: %s", effect, response)
                return True
            _LOGGER.warning("Effect name %s does not exist: %s", effect, response)
            return False  # noqa: TRY300

        except aiohttp.ClientError:
            _LOGGER.exception("Connection error")
            return False
        except Exception:
            _LOGGER.exception("Unexpected error")
            return False
