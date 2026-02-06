# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
