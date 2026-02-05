"""Constants for IKEA OBEGRÄNSAD Led."""

# Base component constants
NAME = "IKEA OBEGRÄNSAD Led"
DOMAIN = "ikea_obegransad_led"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.1.0"

ATTRIBUTION = "Data provided by IKEA OBEGRÄNSAD API for Wall Light with LED Matrix"
ISSUE_URL = "https://github.com/lucaam/ikea-obegransad-led/issues"

# Icons
ICON = "mdi:wall"

# Device classes

# Platforms
LIGHT = "light"
PLATFORMS = [LIGHT]


DEFAULT_EFFECTS = [
    "Draw",
    "Breakout",
    "Snake",
    "GameOfLife",
    "Stars",
    "Lines",
    "Circle",
    "Rain",
    "Firework",
    "Big Clock",
    "Clock",
    "PongClock",
    "Ticking Clock",
    "Weather",
    "Animation",
    "DDP",
]

# Configuration and options
CONF_HOST = "Hostname or IP"
CONF_SCAN_INTERVAL = 30
CONF_DEFAULT_MESSAGE_BACKGROUND_EFFECT = "DDP"
# Defaults
DEFAULT_NAME = "Ikea OBEGRÄNSAD LED Wall Light"


STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This custom integration allows you to control your IKEA OBEGRÄNSAD LED wall light.
You can control the brightness, switch plugins, and display custom messages.
Enjoy using your smart home setup!

For help and documentation, visit the integration's GitHub page.
{ISSUE_URL}
-------------------------------------------------------------------
"""
