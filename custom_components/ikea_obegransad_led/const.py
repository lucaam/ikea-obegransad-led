"""Constants for IKEA OBEGRÄNSAD Led."""

# Base component constants
NAME = "IKEA OBEGRÄNSAD Led"
DOMAIN = "ikea_obegransad_led"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.4.1"

ATTRIBUTION = "Data provided by IKEA OBEGRÄNSAD API for Wall Light with LED Matrix"
ISSUE_URL = "https://github.com/lucaam/ikea-obegransad-led/issues"

# Icons
ICON = "mdi:wall"

# Device classes

# Platforms
LIGHT = "light"
SENSOR = "sensor"
BINARY_SENSOR = "binary_sensor"
BUTTON = "button"
SELECT = "select"
NOTIFY = "notify"
CAMERA = "camera"
PLATFORMS = [LIGHT, BINARY_SENSOR, SENSOR, BUTTON, SELECT, CAMERA]


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
CONF_WEATHER_LOCATION = "Weather Location"
# Defaults
DEFAULT_NAME = "Ikea OBEGRÄNSAD LED Wall Light"

# Service names
SERVICE_SEND_MESSAGE = "send_message"
SERVICE_REMOVE_MESSAGE = "remove_message"
SERVICE_SET_SCHEDULE = "set_schedule"
SERVICE_START_SCHEDULE = "start_schedule"
SERVICE_STOP_SCHEDULE = "stop_schedule"
SERVICE_CLEAR_SCHEDULE = "clear_schedule"
SERVICE_ROTATE_DISPLAY = "rotate_display"
SERVICE_PERSIST_PLUGIN = "persist_plugin"
SERVICE_CLEAR_STORAGE = "clear_storage"
SERVICE_GET_DISPLAY_DATA = "get_display_data"

# Service attributes
ATTR_MESSAGE = "message"
ATTR_MESSAGE_ID = "message_id"
ATTR_REPEAT = "repeat"
ATTR_DELAY = "delay"
ATTR_GRAPH = "graph"
ATTR_MINY = "miny"
ATTR_MAXY = "maxy"
ATTR_DIRECTION = "direction"
ATTR_SCHEDULE = "schedule"

# Rotation directions
DIRECTION_RIGHT = "right"
DIRECTION_LEFT = "left"


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
