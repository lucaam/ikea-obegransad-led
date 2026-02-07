# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.1] - 2026-02-07

## Changes

## :rocket: Features
- Weather Location is now synced via `/api/config` so the sensor shows the device value when not set in the UI
- Config form no longer shows the message background effect (DDP remains default behavior)

## :hammer: Refactoring
- Centralized config read/write helpers in API client for `/api/config`

## :memo: Notes
- Options page removed from UI to avoid empty settings screen
- Host example placeholder is now populated in the setup form

## [0.5.0] - 2026-02-07

### Added

#### Configuration
- **Weather Location**: Optional configuration field to specify weather/location information for future weather plugin integration

#### Sensors
- **Weather Location Sensor**: New sensor entity that displays the configured weather location among other device sensors

#### Icons & Branding
- **Material Design Icons**: SVG icon for use in custom frontends and documentation
- **Material Design PNG Icons**: 24×24 and 48×48 PNG versions for various display contexts
- **HACS Icons**: PNG icons (200×200 and 400×400) with glow effect for HACS marketplace integration
- **SVG Icon**: Scalable vector version of HACS icon for web use

### Changed
- Updated version to 0.5.0
- Enhanced device configuration form with weather location option
- Improved visual presentation in HACS marketplace with branded icons

### Notes
- Weather Location is optional and can be left blank if weather plugin is not planned

## [0.4.1] - 2026-02-07

### Fixed
- Camera entity now initializes tokens correctly to avoid access token errors
- Camera preview normalizes non-256 byte payloads for better resilience
- Clear storage endpoint updated to use /api/storage/clear

### Changed
- Added Pillow to integration requirements for camera rendering

### Notes
- Diagnostic sensors require firmware fields (rssi, uptime, freeHeap, ipAddress, macAddress) in /api/info

## [0.4.0] - 2026-02-07

### Added

#### Sensor Entities
- **Rotation**: Current display rotation (0°, 90°, 180°, 270°)
- **Brightness**: Current brightness as percentage (0-100%)
- **Active Plugin**: Name of the currently active plugin
- **Status**: Device status indicator (NONE, WSBINARY, UPDATE, LOADING)
- **Schedule Count**: Number of scheduled items in queue

#### Diagnostic Sensors
- **WiFi Signal**: Device WiFi signal strength in dBm
- **Uptime**: Device uptime in seconds
- **Free Memory**: Available heap memory in bytes
- **IP Address**: Device network IP address
- **MAC Address**: Device MAC address

#### Button Entities
- **Rotate Right**: Rotate display 90 degrees clockwise
- **Rotate Left**: Rotate display 90 degrees counter-clockwise
- **Persist Plugin**: Save current plugin as boot default
- **Clear Storage**: Clear all device storage
- **Start Schedule**: Start automatic plugin switching
- **Stop Schedule**: Stop automatic plugin switching
- **Clear Schedule**: Clear all scheduled items

#### Select Entity
- **Plugin Selection**: Dropdown to switch active plugin from device page

#### Camera Entity
- **Screen Preview**: Live preview of 16x16 LED matrix display (requires Pillow library)

#### Notify Service
- **notify.ikea_obegransad_led**: Send text messages to display with optional parameters (repeat, delay, graph, message_id)

#### Device Information
- Enhanced device_info with configuration URL and network details
- Diagnostic category for system/network sensors

### Changed
- Updated version to 0.4.0
- Expanded coordinator with diagnostic attributes (wifi_rssi, uptime, free_memory, ip_address, mac_address)
- Enhanced entity organization with proper translation keys

### Technical
- New module: `sensor.py` for state and diagnostic sensors (10 entities)
- New module: `button.py` for quick action buttons (7 entities)
- New module: `select.py` for plugin selection dropdown
- New module: `notify.py` for message notification service
- New module: `camera.py` for LED matrix preview (optional Pillow dependency)
- Updated `const.py` with new platform constants

### Translations
- Added Italian translations for all new entities
- Added English translations for all new entities
- Added Norwegian translations for all new entities
- Added French translations for all new entities

### Notes
- Diagnostic sensors are hidden from main UI but available in diagnostics panel
- Camera entity requires Pillow library: `pip install Pillow`
- All new entities are properly integrated with WebSocket updates
- Sensor data requires firmware support for wifi_rssi, uptime, freeHeap, ipAddress, macAddress fields

## [0.3.0] - 2026-02-06

### Added

#### WebSocket Integration
- Live WebSocket connection to the device (`ws://{host}/ws`)
- Automatic reconnection with exponential backoff (max 5 minutes)
- Real-time state updates from `event: "info"` payloads
- WebSocket-backed `rotate_display` and `persist_plugin` services

### Changed

- Updated version to 0.3.0
- Coordinator now consumes WebSocket push updates for instant UI refresh

### Notes

- REST polling remains enabled as a fallback
- WebSocket connection required for rotation and persistence services

## [0.2.0] - 2026-02-06

### Added

#### Services
- **send_message**: Enhanced with graph support, miny/maxy parameters, and message_id
- **remove_message**: Remove specific messages from display by ID
- **set_schedule**: Set automatic plugin switching schedule
- **start_schedule**: Start the plugin schedule
- **stop_schedule**: Stop the plugin schedule  
- **clear_schedule**: Clear the plugin schedule completely
- **rotate_display**: Rotate display 90 degrees (WebSocket required, stub)
- **persist_plugin**: Save current plugin as default on boot (WebSocket required, stub)
- **clear_storage**: Clear device storage
- **get_display_data**: Retrieve raw display data (256 bytes)

#### Features
- Plugin scheduler support with automatic switching
- Binary sensor entity for schedule active status
- Graph display support in messages
- Display rotation and plugin persistence planned (requires WebSocket)
- WebSocket client foundation for future real-time updates

#### API Enhancements
- Added all REST API endpoints from C++ firmware
- Extended API client with scheduler methods
- Added rotation and persistence method stubs (WebSocket)
- Enhanced message sending with graph support
- Added storage management methods

#### State Attributes
- `rotation`: Current display rotation
- `persist_plugin`: ID of persisted plugin
- `schedule_active`: Whether schedule is running
- `schedule`: Array of schedule items with pluginId and duration
- `rows`: Display rows (16)
- `cols`: Display columns (16)
- `status`: Current device status

#### Entities
- Binary sensor for schedule status with schedule details in attributes

#### Translations
- Added Italian translations for all new services
- Added English translations for all new services
- Extended strings.json with all service definitions

#### Documentation
- Comprehensive README with all features
- Service usage examples
- Example automations for common use cases
- API reference documentation
- Troubleshooting guide

### Changed
- Updated version to 0.2.0
- Enhanced coordinator to track all firmware state
- Improved data synchronization with device
- Better error handling and logging

### Technical
- New module: `binary_sensor.py` for schedule status sensor
- New module: `websocket.py` for WebSocket communication (foundation)
- Extended `const.py` with service and attribute constants
- Enhanced `api.py` with 10+ new methods
- Updated `light.py` with extra_state_attributes property
- Refactored service handlers in `__init__.py`

### Notes
- WebSocket features (rotate_display, persist_plugin) require persistent WebSocket connection
- Full WebSocket implementation planned for future release
- All REST API endpoints from C++ firmware now supported
- Integration now mirrors 100% of firmware features via REST API

## [0.1.0] - Initial Release

### Added
- Basic light entity with on/off control
- Brightness control (0-255)
- Effect/plugin switching
- Send message service with text, repeat, and delay
- Configuration flow
- HACS support
- Multi-language support (English, Italian)

---

For detailed information about the firmware API, see [ph1p/ikea-led-obegraensad](https://github.com/ph1p/ikea-led-obegraensad)
