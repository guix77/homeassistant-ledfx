# LedFx Home Assistant Integration — CLAUDE.md

## Context

Custom HA integration for LedFx, based on [integration_blueprint](https://github.com/ludeeus/integration_blueprint).

- **DOMAIN**: `ledfx`
- **LedFx host**: `http://nestor.home:8888`
- The integration previously exposed a custom `media_player` (play/pause) — **removed**, replaced by scene switches.

---

## Goal: expose one `switch` per LedFx scene

Each LedFx scene is exposed as a `switch` entity in HA.

### ON behavior (activation)

1. `GET /api/scenes` → fetch the target scene's virtuals
2. Filter virtuals to activate:
   - If the scene has an `action` field per virtual → keep only those with `action: "activate"`
   - Otherwise (no `action` field) → keep all virtuals with a non-empty `config` (`{}` = skip)
3. For each retained virtual → `POST /api/devices/{virtual_id}` with empty payload `{}`
   - On error (device not found, hostname unresolvable) → log a warning in HA and continue
4. `PUT /api/scenes` with `{"id": "<scene_id>", "action": "activate"}`

### OFF behavior (deactivation)

`PUT /api/scenes` with `{"id": "<scene_id>", "action": "deactivate"}`

This releases the WLED devices (they resume their autonomous behavior).

### Switch state

`active` field in `GET /api/scenes` → `true` = ON, `false` = OFF.

---

## Verified LedFx API endpoints

### GET /api/scenes
```
GET http://nestor.home:8888/api/scenes
```
Returns all scenes with their virtuals and `active` state.

Scene structure:
- Old-style scene (no `action` field): virtuals have just `config` + `type`
- New-style scene (with `action` field): virtuals have `action: "activate"` or `action: "ignore"`
- In both cases, skip virtuals with empty config `{}`

### POST /api/devices/{id}
```
POST http://nestor.home:8888/api/devices/{virtual_id}
Body: {}
```
Triggers `resolve_address()` + `device.activate()` on the LedFx side.

**Why this is necessary**: at LedFx boot, a device gets `online: false` if its hostname cannot be resolved (`socket.getaddrinfo` fails). The POST forces a new resolution attempt and activates the stream to the WLED.

**Important**: `online: false` has nothing to do with the physical state of the LEDs. It is purely a DNS/hostname resolution issue at LedFx boot time. Always POST to all devices in the scene, without filtering on `online`.

The device ID equals the virtual ID in the scene (they are identical).

### PUT /api/scenes
```
PUT http://nestor.home:8888/api/scenes
Body: {"id": "<scene_id>", "action": "activate"}
Body: {"id": "<scene_id>", "action": "deactivate"}
```

---

## What needs to be implemented

### `switch` platform

- Fetch scenes at startup via the coordinator
- One `switch` entity per scene
- Switch name = `scene["name"]`
- Switch ID = `scene_id` (LedFx slug)
- Poll state via `GET /api/scenes`

### Remove the media_player

The existing `media_player` component must be removed — global play/pause is replaced by scene switches (deactivating a scene releases the devices, equivalent to pause).

---

## Project structure

Based on [integration_blueprint](https://github.com/ludeeus/integration_blueprint).

```python
DOMAIN = "ledfx"
```

---

## Sample GET /api/scenes response (excerpts)

```json
{
  "status": "success",
  "scenes": {
    "music-1": {
      "name": "Music 1",
      "virtuals": {
        "niche-spot-centre": {
          "config": { "...": "..." },
          "type": "magnitude"
        },
        "niche-strips": {}
      },
      "active": true
    },
    "music-with-dining": {
      "name": "Music with dining",
      "virtuals": {
        "niche-spot-centre": {
          "action": "activate",
          "config": { "...": "..." },
          "type": "magnitude"
        },
        "escalier": {
          "action": "ignore",
          "config": {},
          "type": ""
        }
      },
      "active": false
    }
  }
}
```