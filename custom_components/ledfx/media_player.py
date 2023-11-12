"""Media player component."""
from __future__ import annotations

from homeassistant.components.media_player import (
    MediaPlayerEntity,
    MediaPlayerEntityDescription,
    MediaPlayerEntityFeature,
    MediaPlayerState,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import LedfxDataUpdateCoordinator
from .entity import LedfxEntity

ENTITY_DESCRIPTIONS = (
    MediaPlayerEntityDescription(
        key="media_player",
        name="LedFx media player",
        icon="mdi:led-strip-variant",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    add_entities_callback: AddEntitiesCallback,
) -> None:
    """Set up the media_player platform."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    add_entities_callback(
        LedfxMediaPlayer(
            coordinator=coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class LedfxMediaPlayer(LedfxEntity, MediaPlayerEntity):
    """Ledfx media player entry."""

    def __init__(
        self,
        coordinator: LedfxDataUpdateCoordinator,
        entity_description: MediaPlayerEntityDescription,
    ) -> None:
        """Initialize the media player class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._supported_features = (
            MediaPlayerEntityFeature.PLAY
            | MediaPlayerEntityFeature.PAUSE
        )

    @property
    def supported_features(self) -> MediaPlayerEntityFeature:
        """Supported features."""
        return self._supported_features

    @property
    def state(self) -> MediaPlayerState | None:
        """Return current state."""
        if self.coordinator.data.get("virtuals")["paused"]:
            return MediaPlayerState.PAUSED
        return MediaPlayerState.PLAYING

    async def async_media_play(self) -> None:
        """Play media."""
        if self.coordinator.data.get("virtuals")["paused"]:
            await self.coordinator.client.async_toggle_pause()
            await self.coordinator.async_request_refresh()

    async def async_media_pause(self) -> None:
        """Pause media."""
        if not self.coordinator.data.get("virtuals")["paused"]:
            await self.coordinator.client.async_toggle_pause()
            await self.coordinator.async_request_refresh()
