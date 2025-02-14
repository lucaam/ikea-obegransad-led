"""
Custom integration to integrate IKEA OBEGRÄNSAD Led with Home Assistant.

For more details about this integration, please refer to
https://github.com/lucaam/ikea-obegransad-led
"""

import asyncio
import logging
from datetime import timedelta

import homeassistant.helpers.config_validation as cv
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN

SCAN_INTERVAL = timedelta(seconds=30)

_LOGGER: logging.Logger = logging.getLogger(__package__)

# Schema di configurazione vuoto
CONFIG_SCHEMA = cv.empty_config_schema


# Integration setup
async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the IKEA OBEGRÄNSAD Led integration."""
    _LOGGER.info(f"Setting up {DOMAIN} integration.")
    return True


# Questo viene chiamato quando viene creata una voce di configurazione o l'utente imposta l'integrazione tramite UI
async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up the IKEA OBEGRÄNSAD Led integration from a config entry."""
    _LOGGER.info(f"Setting up IKEA OBEGRÄNSAD Led from config entry: {entry.title}")

    # Aggiungi le piattaforme
    for platform in entry.options:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    _LOGGER.info(f"Unloading IKEA OBEGRÄNSAD Led config entry: {entry.title}")

    # Scarica tutte le piattaforme associate all'entry
    unloaded = await asyncio.gather(
        *[
            hass.config_entries.async_forward_entry_unload(entry, platform)
            for platform in entry.options
        ]
    )

    # Pulisci i dati associati all'entry
    hass.data[DOMAIN].pop(entry.entry_id, None)

    return all(unloaded)
