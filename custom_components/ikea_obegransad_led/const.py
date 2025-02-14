from datetime import timedelta

"""Constants for IKEA OBEGRÄNSAD Led."""

# Base component constants
NAME = "IKEA OBEGRÄNSAD Led"
DOMAIN = "ikea_obegransad_led"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.0.1"

ATTRIBUTION = "Data provided by IKEA OBEGRÄNSAD API for Wall Light with LED Matrix"
ISSUE_URL = "https://github.com/lucaam/ikea-obegransad-led/issues"

# Icons
ICON = "mdi:wall-sconce"

# Device classes
BINARY_SENSOR_DEVICE_CLASS = "connectivity"

# Platforms
BINARY_SENSOR = "binary_sensor"
SENSOR = "sensor"
SWITCH = "switch"
LIGHT = "light"
PLATFORMS = [BINARY_SENSOR, SENSOR, SWITCH]

SCAN_INTERVAL = timedelta(seconds=60)

# Configuration and options
CONF_ENABLED = "enabled"
CONF_HOST = "host"

# Defaults
DEFAULT_NAME = "Ikea OBEGRÄNSAD LED Wall Light"


STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This custom integration allows you to control your IKEA OBEGRÄNSAD LED wall light with a matrix of LEDs.
You can control the brightness, switch plugins, and display custom messages.
Enjoy using your smart home setup!

For help and documentation, visit the integration's GitHub page.
{ISSUE_URL}
-------------------------------------------------------------------
"""
