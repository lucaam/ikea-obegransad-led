# IKEA OBEGRÄNSAD LED - Automation Examples

This file contains example automations demonstrating the full capabilities of the integration.

## Table of Contents

- [Basic Control](#basic-control)
- [Messages & Graphs](#messages--graphs)
- [Scheduling](#scheduling)
- [Advanced Examples](#advanced-examples)

## Basic Control

### Adjust Brightness Based on Sun Position

```yaml
automation:
  - alias: "OBEGRÄNSAD - Brightness High at Sunrise"
    trigger:
      - platform: sun
        event: sunrise
        offset: "00:30:00"
    action:
      - service: light.turn_on
        target:
          entity_id: light.ikea_obegraensad_led_wall_light
        data:
          brightness: 200

  - alias: "OBEGRÄNSAD - Brightness Low at Sunset"
    trigger:
      - platform: sun
        event: sunset
        offset: "-00:30:00"
    action:
      - service: light.turn_on
        target:
          entity_id: light.ikea_obegraensad_led_wall_light
        data:
          brightness: 50
```

### Switch Effects Based on Time of Day

```yaml
automation:
  - alias: "OBEGRÄNSAD - Morning Clock"
    trigger:
      - platform: time
        at: "06:00:00"
    action:
      - service: light.turn_on
        target:
          entity_id: light.ikea_obegraensad_led_wall_light
        data:
          effect: "Clock"

  - alias: "OBEGRÄNSAD - Evening Stars"
    trigger:
      - platform: time
        at: "20:00:00"
    action:
      - service: light.turn_on
        target:
          entity_id: light.ikea_obegraensad_led_wall_light
        data:
          effect: "Stars"
```

## Messages & Graphs

### Display Welcome Message

```yaml
automation:
  - alias: "OBEGRÄNSAD - Welcome Home"
    trigger:
      - platform: state
        entity_id: person.john
        to: "home"
    action:
      - service: ikea_obegransad_led.send_message
        data:
          message: "Welcome Home!"
          repeat: 2
          delay: 60
```

### Display Temperature Graph

```yaml
automation:
  - alias: "OBEGRÄNSAD - Temperature Graph every hour"
    trigger:
      - platform: time_pattern
        hours: "/1"
    action:
      - service: ikea_obegransad_led.send_message
        data:
          message: "Temp"
          graph: >
            {% set history = state_attr('sensor.outdoor_temperature', 'history') %}
            {% set temps = history[-16:] | map(attribute='state') | map('float') | list %}
            {{ temps | join(',') }}
          miny: 0
          maxy: 30
          repeat: 1
          delay: 50
          message_id: "temp_graph"
```

### Display Energy Consumption Graph

```yaml
automation:
  - alias: "OBEGRÄNSAD - Energy Graph"
    trigger:
      - platform: time
        at: "08:00:00"
      - platform: time
        at: "20:00:00"
    action:
      - service: ikea_obegransad_led.send_message
        data:
          message: "kWh"
          graph: >
            {% set history = states.sensor.energy_consumption.last_changed %}
            8,9,7,10,12,14,13,11,9,8,7,6,8,9,10,11
          miny: 0
          maxy: 15
          repeat: 2
          delay: 40
          message_id: "energy_graph"
```

### Remove Message When Condition Met

```yaml
automation:
  - alias: "OBEGRÄNSAD - Clear Alert When Resolved"
    trigger:
      - platform: state
        entity_id: binary_sensor.door_open
        to: "off"
    action:
      - service: ikea_obegransad_led.remove_message
        data:
          message_id: "door_alert"
```

## Scheduling

### Daytime Schedule - Useful Effects

```yaml
automation:
  - alias: "OBEGRÄNSAD - Daytime Schedule"
    trigger:
      - platform: time
        at: "08:00:00"
    action:
      - service: ikea_obegransad_led.set_schedule
        data:
          schedule: >
            [
              {"pluginId": 10, "duration": 1800},
              {"pluginId": 13, "duration": 1800}
            ]
      - service: ikea_obegransad_led.start_schedule
```

### Evening Schedule - Ambient Effects

```yaml
automation:
  - alias: "OBEGRÄNSAD - Evening Schedule"
    trigger:
      - platform: sun
        event: sunset
    action:
      - service: ikea_obegransad_led.set_schedule
        data:
          schedule: >
            [
              {"pluginId": 4, "duration": 300},
              {"pluginId": 5, "duration": 300},
              {"pluginId": 8, "duration": 300}
            ]
      - service: ikea_obegransad_led.start_schedule
```

### Stop Schedule at Bedtime

```yaml
automation:
  - alias: "OBEGRÄNSAD - Stop Schedule at Night"
    trigger:
      - platform: time
        at: "23:00:00"
    action:
      - service: ikea_obegransad_led.stop_schedule
      - service: light.turn_on
        target:
          entity_id: light.ikea_obegraensad_led_wall_light
        data:
          effect: "Clock"
          brightness: 30
```

### Clear Schedule on Manual Override

```yaml
automation:
  - alias: "OBEGRÄNSAD - Clear Schedule on Manual Change"
    trigger:
      - platform: state
        entity_id: light.ikea_obegraensad_led_wall_light
        attribute: effect
    condition:
      - condition: state
        entity_id: binary_sensor.ikea_obegraensad_led_wall_light_schedule_active
        state: "on"
    action:
      - service: ikea_obegransad_led.clear_schedule
```

## Advanced Examples

### Weather-Based Display

```yaml
automation:
  - alias: "OBEGRÄNSAD - Weather Display"
    trigger:
      - platform: time_pattern
        hours: "/3"
    action:
      - choose:
          - conditions:
              - condition: state
                entity_id: weather.home
                state: "sunny"
            sequence:
              - service: light.turn_on
                target:
                  entity_id: light.ikea_obegraensad_led_wall_light
                data:
                  effect: "Stars"
                  brightness: 255
          - conditions:
              - condition: state
                entity_id: weather.home
                state: "rainy"
            sequence:
              - service: light.turn_on
                target:
                  entity_id: light.ikea_obegraensad_led_wall_light
                data:
                  effect: "Rain"
                  brightness: 150
          - conditions:
              - condition: state
                entity_id: weather.home
                state: "cloudy"
            sequence:
              - service: light.turn_on
                target:
                  entity_id: light.ikea_obegraensad_led_wall_light
                data:
                  effect: "Lines"
                  brightness: 180
```

### Smart Notification System

```yaml
automation:
  - alias: "OBEGRÄNSAD - Package Delivered"
    trigger:
      - platform: state
        entity_id: sensor.package_status
        to: "delivered"
    action:
      - service: ikea_obegransad_led.send_message
        data:
          message: "Package Delivered!"
          repeat: 5
          delay: 50
          message_id: "package_notif"
      - delay:
          minutes: 30
      - service: ikea_obegransad_led.remove_message
        data:
          message_id: "package_notif"

  - alias: "OBEGRÄNSAD - Doorbell Ring"
    trigger:
      - platform: state
        entity_id: binary_sensor.doorbell
        to: "on"
    action:
      - service: ikea_obegransad_led.send_message
        data:
          message: "Doorbell!"
          repeat: 3
          delay: 30
          message_id: "doorbell"
      - service: light.turn_on
        target:
          entity_id: light.ikea_obegraensad_led_wall_light
        data:
          brightness: 255
```

### Workout Timer with Graph

```yaml
automation:
  - alias: "OBEGRÄNSAD - Workout Progress"
    trigger:
      - platform: state
        entity_id: input_boolean.workout_mode
        to: "on"
    action:
      - repeat:
          while:
            - condition: state
              entity_id: input_boolean.workout_mode
              state: "on"
          sequence:
            - service: ikea_obegransad_led.send_message
              data:
                message: "HR"
                graph: >
                  {% set hr = states('sensor.heart_rate') | int %}
                  {% set normalized = ((hr - 60) / 120 * 15) | int %}
                  {{ range(16) | map('random', normalized-2, normalized+2) | list | join(',') }}
                miny: 0
                maxy: 15
                repeat: 1
                delay: 100
                message_id: "workout_hr"
            - delay:
                seconds: 5
```

### Presence-Based Scheduling

```yaml
automation:
  - alias: "OBEGRÄNSAD - Home Schedule"
    trigger:
      - platform: state
        entity_id: group.all_persons
        to: "home"
    action:
      - service: ikea_obegransad_led.set_schedule
        data:
          schedule: >
            [
              {"pluginId": 14, "duration": 600},
              {"pluginId": 10, "duration": 600},
              {"pluginId": 11, "duration": 600}
            ]
      - service: ikea_obegransad_led.start_schedule

  - alias: "OBEGRÄNSAD - Away Mode"
    trigger:
      - platform: state
        entity_id: group.all_persons
        to: "not_home"
        for:
          minutes: 10
    action:
      - service: ikea_obegransad_led.clear_schedule
      - service: light.turn_off
        target:
          entity_id: light.ikea_obegraensad_led_wall_light
```

### Persist Favorite Effect

```yaml
automation:
  - alias: "OBEGRÄNSAD - Save Favorite Effect"
    trigger:
      - platform: event
        event_type: ikea_obegransad_save_effect
    action:
      - service: ikea_obegransad_led.persist_plugin
      - service: persistent_notification.create
        data:
          title: "OBEGRÄNSAD"
          message: "Current effect saved as default!"
```

### Storage Maintenance

```yaml
automation:
  - alias: "OBEGRÄNSAD - Monthly Storage Clear"
    trigger:
      - platform: time
        at: "03:00:00"
    condition:
      - condition: template
        value_template: "{{ now().day == 1 }}"
    action:
      - service: ikea_obegransad_led.clear_storage
      - service: system_log.write
        data:
          message: "OBEGRÄNSAD storage cleared"
          level: info
```

## Lovelace Card Examples

### Basic Control Card

```yaml
type: entities
title: OBEGRÄNSAD LED
entities:
  - entity: light.ikea_obegraensad_led_wall_light
    name: Display
  - entity: binary_sensor.ikea_obegraensad_led_wall_light_schedule_active
    name: Schedule Active
  - type: attribute
    entity: light.ikea_obegraensad_led_wall_light
    attribute: rotation
    name: Rotation
  - type: attribute
    entity: light.ikea_obegraensad_led_wall_light
    attribute: status
    name: Status
```

### Quick Message Card

```yaml
type: vertical-stack
cards:
  - type: entities
    title: Send Message
    entities:
      - entity: input_text.ikea_message
        name: Message
  - type: button
    name: Send
    tap_action:
      action: call-service
      service: ikea_obegransad_led.send_message
      service_data:
        message: "{{ states('input_text.ikea_message') }}"
        repeat: 2
        delay: 60
```

### Schedule Control Card

```yaml
type: entities
title: Schedule Control
entities:
  - entity: binary_sensor.ikea_obegraensad_led_wall_light_schedule_active
    name: Schedule Status
  - type: button
    name: Start Schedule
    tap_action:
      action: call-service
      service: ikea_obegransad_led.start_schedule
  - type: button
    name: Stop Schedule
    tap_action:
      action: call-service
      service: ikea_obegransad_led.stop_schedule
  - type: button
    name: Clear Schedule
    tap_action:
      action: call-service
      service: ikea_obegransad_led.clear_schedule
```

## Node-RED Examples

### Temperature Monitor Flow

```json
[
  {
    "id": "temp_monitor",
    "type": "inject",
    "repeat": "900",
    "name": "Every 15 min"
  },
  {
    "id": "get_temp",
    "type": "api-current-state",
    "entity_id": "sensor.outdoor_temperature"
  },
  {
    "id": "format_graph",
    "type": "function",
    "func": "const temps = flow.get('temp_history') || [];\ntemps.push(parseFloat(msg.data.state));\nif (temps.length > 16) temps.shift();\nflow.set('temp_history', temps);\nmsg.payload = {\n  message: 'Temp',\n  graph: temps.join(','),\n  miny: 0,\n  maxy: 30,\n  repeat: 1,\n  delay: 50\n};\nreturn msg;"
  },
  {
    "id": "send_message",
    "type": "api-call-service",
    "service_domain": "ikea_obegransad_led",
    "service": "send_message"
  }
]
```

---

For more information, see the [README](README.md) and [firmware documentation](https://github.com/ph1p/ikea-led-obegraensad).
