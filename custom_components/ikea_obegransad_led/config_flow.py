"""Adds config flow for IKEA OBEGRÄNSAD Led."""

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from .api import IkeaObegransadLedApiClient
from .const import CONF_HOST
from .const import DOMAIN


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
            valid = await self._test_credentials(user_input[CONF_HOST])
            if valid:
                return self.async_create_entry(
                    title=user_input[CONF_HOST], data=user_input
                )
            else:
                self._errors["base"] = "auth"

            return await self._show_config_form(user_input)

        return await self._show_config_form(user_input)

    async def _show_config_form(self, user_input):
        """Show the configuration form to edit location data."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST): str,  # Solo host ora
                }
            ),
            errors=self._errors,
        )

    async def _test_credentials(self, host):
        """Return true if the host is valid."""
        try:
            session = async_create_clientsession(self.hass)
            client = IkeaObegransadLedApiClient(session, host)
            await client.async_get_info()  # Usa un metodo valido per testare l'host
            return True
        except Exception:
            pass
        return False


class IkeaObegransadLedOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options for ikea_obegransad_led."""

    def __init__(self, config_entry):
        """Initialize options flow handler."""
        self.config_entry = config_entry
        self._errors = {}

    async def async_step_init(self, user_input=None):
        """Manage the options for IKEA OBEGRÄNSAD Led."""
        if user_input is not None:
            # Se vuoi aggiornare le opzioni, inserisci qui la logica
            return self.async_create_entry(title="Options Updated", data=user_input)

        # Aggiungi qui l'interfaccia utente per le opzioni (se necessario)
        return self.async_show_form(
            step_id="init", data_schema=vol.Schema({vol.Optional("option_key"): str})
        )
