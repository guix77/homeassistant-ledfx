"""LedfxEntity class."""
from __future__ import annotations

from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTRIBUTION, DOMAIN, NAME
from .coordinator import LedfxDataUpdateCoordinator


class LedfxEntity(CoordinatorEntity):
    """LedfxEntity class."""

    _attr_attribution = ATTRIBUTION

    def __init__(self, coordinator: LedfxDataUpdateCoordinator) -> None:
        """Initialize."""
        super().__init__(coordinator)
        coordinator._async_update_data()
        self._attr_unique_id = coordinator.config_entry.entry_id
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self.unique_id)},
            name=NAME,
            sw_version=coordinator.data.get("info")["version"]
        )
