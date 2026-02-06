<p>
  <img alt="GitHub Release" src="https://img.shields.io/github/v/release/lucaam/ikea-obegransad-led">
  <img alt="GitHub License" src="https://img.shields.io/github/license/lucaam/ikea-obegransad-led">
  <a href="https://github.com/lucaam/ikea-obegransad-led/issues"><img alt="GitHub Issues" src="https://img.shields.io/github/issues/lucaam/ikea-obegransad-led"></a>
</p>

# IKEA OBEGRÄNSAD Led

Home Assistant integration to control IKEA OBEGRÄNSAD Wall Lamp hacked with [ph1p/ikea-led-obegraensad](https://github.com/ph1p/ikea-led-obegraensad) and an ESP32 device.

## ✨ Features

### Device Control
- [x] Turn the lamp on and off
- [x] Adjust light intensity (brightness 0-255)
- [x] Switch between available plugins/effects
- [ ] Display rotation (0°, 90°, 180°, 270°) *
- [ ] Persist current plugin as default *

### Messages & Display
- [x] Send text messages with custom repeat and delay
- [x] Display graphs alongside text messages
- [x] Remove specific messages by ID
- [x] Get raw display data (256 bytes for 16x16 matrix)

### Scheduling
- [x] Set automatic plugin switching schedule
- [x] Start/stop/clear schedule
- [x] Binary sensor for schedule status
- [x] View schedule details in attributes

### Additional Features
- [x] Extra state attributes (rotation, schedule, status, rows, cols)
- [x] Full REST API support
- [ ] WebSocket support for real-time updates *
- [x] Clear device storage
- [x] Local polling integration

<sup>* Requires WebSocket connection (planned for 0.3.0)</sup>

## 📦 Installation

The installation is made easy with the Home Assistant Community Store (HACS):

1. Open the Home Assistant Community Store
2. Add this repository using the following URL: `https://github.com/lucaam/ikea-obegransad-led`
3. Once added, navigate to **Configuration > Integrations** and look for `IKEA OBEGRÄNSAD Led`
4. Configure the integration by providing:
   - **Hostname or IP address** of your device
   - **Default animation for messages** (default: DDP)

## 🚀 Usage

### Basic Control

The integration creates a light entity that supports:

- **Power**: Turn on/off
- **Brightness**: 0-255
- **Effects**: All available plugins from your device

### Services

#### Send Message

Display a text message on the LED matrix:

```yaml
service: ikea_obegransad_led.send_message
data:
  message: "Hello World!"
  repeat: 3
  delay: 70
```

With graph data:

```yaml
service: ikea_obegransad_led.send_message
data:
  message: "Temperature"
  graph: "8,5,2,1,0,0,1,4,7,10,13,14,15,15,14,11"
  miny: 0
  maxy: 15
  repeat: 1
  delay: 50
  message_id: "temp_graph_1"
```

#### Remove Message

Remove a specific message:

```yaml
service: ikea_obegransad_led.remove_message
data:
  message_id: "temp_graph_1"
```

#### Set Schedule

Automatically switch between plugins:

```yaml
service: ikea_obegransad_led.set_schedule
data:
  schedule: '[{"pluginId": 2, "duration": 60}, {"pluginId": 4, "duration": 120}]'
```

#### Control Schedule

```yaml
# Start schedule
service: ikea_obegransad_led.start_schedule

# Stop schedule
service: ikea_obegransad_led.stop_schedule

# Clear schedule
service: ikea_obegransad_led.clear_schedule
```

#### Rotate Display

Requires WebSocket support (available in 0.3.0).

```yaml
service: ikea_obegransad_led.rotate_display
data:
  direction: "right"  # or "left"
```

#### Persist Plugin

Requires WebSocket support (available in 0.3.0).

Save the current plugin as default:

```yaml
service: ikea_obegransad_led.persist_plugin
```

#### Clear Storage

Clear device storage:

```yaml
service: ikea_obegransad_led.clear_storage
```

#### Get Display Data

Retrieve raw display data:

```yaml
service: ikea_obegransad_led.get_display_data
```

### Entities

#### Light Entity

Main control entity with attributes:

- `brightness`: Current brightness (0-255)
- `effect`: Current active plugin/effect
- `effect_list`: List of available plugins
- `rotation`: Display rotation (0, 1, 2, 3 = 0°, 90°, 180°, 270°)
- `persist_plugin`: ID of persisted plugin
- `schedule_active`: Whether schedule is running
- `schedule`: Array of schedule items
- `rows`: Display rows (16)
- `cols`: Display columns (16)
- `status`: Current device status

#### Binary Sensor Entity

A binary sensor indicating if the plugin schedule is active:

- **State**: `on` when schedule is running, `off` otherwise
- **Attributes**:
  - `schedule`: Current schedule configuration
  - `schedule_count`: Number of items in schedule

### Example Automations

#### Display Temperature Graph

```yaml
automation:
  - alias: "Display Temperature Graph"
    trigger:
      - platform: time_pattern
        minutes: "/15"
    action:
      - service: ikea_obegransad_led.send_message
        data:
          message: "Temp"
          graph: >
            {% set temps = state_attr('sensor.temperature_history', 'values') %}
            {{ temps | join(',') }}
          miny: 15
          maxy: 30
          repeat: 2
```

#### Cycle Through Effects at Night

```yaml
automation:
  - alias: "Night Effect Rotation"
    trigger:
      - platform: sun
        event: sunset
    action:
      - service: ikea_obegransad_led.set_schedule
        data:
          schedule: '[{"pluginId": 5, "duration": 300}, {"pluginId": 8, "duration": 300}]'
      - service: ikea_obegransad_led.start_schedule
```

#### Stop Schedule at Sunrise

```yaml
automation:
  - alias: "Stop Schedule at Sunrise"
    trigger:
      - platform: sun
        event: sunrise
    action:
      - service: ikea_obegransad_led.stop_schedule
```

## 🔧 API Reference

The integration mirrors the [C++ firmware API](https://github.com/ph1p/ikea-led-obegraensad#http-api-reference):

- `GET /api/info` - Device information
- `PATCH /api/plugin?id={id}` - Set plugin
- `PATCH /api/brightness?value={value}` - Set brightness  
- `GET /api/message?text=...` - Send message
- `GET /api/removemessage?id={id}` - Remove message
- `POST /api/schedule` - Set schedule
- `GET /api/schedule/start` - Start schedule
- `GET /api/schedule/stop` - Stop schedule
- `GET /api/schedule/clear` - Clear schedule
- `GET /api/clearstorage` - Clear storage
- `GET /api/data` - Get display data

WebSocket endpoint: `ws://{host}/ws` (planned for future releases)

## 🐛 Troubleshooting

### Device Not Found

- Verify the IP address/hostname is correct
- Ensure the device is on the same network
- Check that the firmware is properly flashed

### Effects Not Working

- Verify your firmware has the required plugins
- Check the logs for any API errors
- Ensure the device is accessible via HTTP

### Schedule Not Starting

- Verify the schedule JSON format is correct
- Check that plugin IDs exist on your device
- View the binary sensor state for schedule status

## 🤝 Contributing

Any contributions you make are **greatly appreciated**. Please read [CONTRIBUTING.md](https://github.com/lucaam/ikea-obegransad-led/blob/main/CONTRIBUTING.md) for details on the code of conduct and the process for submitting pull requests.

## 📝 Versioning

[SemVer](http://semver.org/) is used for versioning. For the versions available, see the [tags on this repository](https://github.com/lucaam/ikea-obegransad-led/tags).

## 👥 Authors

- **Luca Amoriello** - [@lucaam](https://github.com/lucaam)

See also the list of [contributors](https://github.com/lucaam/ikea-obegransad-led/contributors) who participated in this project.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## 🙏 Acknowledgments

- [💡 IKEA OBEGRÄNSAD LED Wall Lamp](https://www.ikea.com/it/it/p/obegraensad-lampada-da-parete-a-led-nero-00526248/)
- [🔧 ph1p's ikea-led-obegraensad Project](https://github.com/ph1p/ikea-led-obegraensad)
- [🏠 Home Assistant](https://www.home-assistant.io/)
- [🤖 ChatGPT](https://chatgpt.com/)
