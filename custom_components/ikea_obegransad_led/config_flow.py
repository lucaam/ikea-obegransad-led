import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_create_clientsession
import aiohttp

from .api import IkeaObegransadLedApiClient
from .const import CONF_HOST, DOMAIN

_LOGGER = logging.getLogger(__name__)


class IkeaObegransadLedFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for ikea_obegransad_led."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH

    def __init__(self):
        """Initialize."""
        self._errors = {}

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        self._errors = {}

        if user_input is not None:
            host = user_input[CONF_HOST]
            valid = await self._test_credentials(host)
            if valid:
                return self.async_create_entry(title=host, data=user_input)
            else:
                self._errors["base"] = "cannot_connect"

            return await self._show_config_form(user_input)

        return await self._show_config_form(user_input)

    async def _show_config_form(self, user_input):
        """Show the configuration form to edit location data."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required(CONF_HOST): str}),
            errors=self._errors,
        )

    async def _test_credentials(self, host):
        """Return true if the host is valid."""
        try:
            _LOGGER.debug("Testing connection to %s", host)
            session = async_create_clientsession(self.hass)
            client = IkeaObegransadLedApiClient(session, host)
            response = await client.get_info()  # Corrected method name

            if response:
                _LOGGER.debug("Received valid response: %s", response)
                return True
            else:
                _LOGGER.warning("Invalid response received: %s", response)
                return False

        except aiohttp.ClientError as err:
            _LOGGER.error("Connection error: %s", err)
        except Exception as err:
            _LOGGER.exception("Unexpected error: %s", err)

        return False
