"""Switch platform for LedFx scenes."""
from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, LOGGER
from .coordinator import LedfxDataUpdateCoordinator
from .entity import LedfxEntity


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the switch platform."""
    coordinator: LedfxDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    scenes = coordinator.data.get("scenes", {}).get("scenes", {})
    async_add_entities(
        LedfxSceneSwitch(coordinator=coordinator, scene_id=scene_id)
        for scene_id in scenes
    )


class LedfxSceneSwitch(LedfxEntity, SwitchEntity):
    """LedFx scene switch entity."""

    def __init__(
        self,
        coordinator: LedfxDataUpdateCoordinator,
        scene_id: str,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self._scene_id = scene_id
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_{scene_id}"
        self._attr_icon = "mdi:led-strip-variant"

    def _scene(self) -> dict:
        return self.coordinator.data.get("scenes", {}).get("scenes", {}).get(self._scene_id, {})

    @property
    def name(self) -> str:
        """Return the scene name."""
        return self._scene().get("name", self._scene_id)

    @property
    def is_on(self) -> bool:
        """Return true when the scene is active."""
        return bool(self._scene().get("active", False))

    async def async_turn_on(self, **kwargs) -> None:
        """Activate the scene."""
        virtuals = self._scene().get("virtuals", {})

        has_action_field = any("action" in v for v in virtuals.values())
        if has_action_field:
            to_activate = [vid for vid, v in virtuals.items() if v.get("action") == "activate"]
        else:
            to_activate = [vid for vid, v in virtuals.items() if v.get("config", {})]

        for virtual_id in to_activate:
            try:
                await self.coordinator.client.async_activate_device(virtual_id)
            except Exception:  # pylint: disable=broad-except
                LOGGER.warning("Failed to activate device %s, continuing", virtual_id)

        await self.coordinator.client.async_activate_scene(self._scene_id)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs) -> None:
        """Deactivate the scene."""
        await self.coordinator.client.async_deactivate_scene(self._scene_id)
        await self.coordinator.async_request_refresh()
