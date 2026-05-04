"""Enigma2 EPG Camera – Pseudo-Live-Bild via Grab-URL (konfigurierbare Refresh-Rate)."""
from __future__ import annotations

from homeassistant.components.camera import Camera
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import DOMAIN
from .coordinator import Enigma2EPGCoordinator
from .sensor import _device_info


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([Enigma2Camera(coordinator, entry)])


class Enigma2Camera(CoordinatorEntity, Camera):
    _attr_has_entity_name = True
    _attr_name = "TV"
    _attr_icon = "mdi:television-play"

    def __init__(self, coordinator: Enigma2EPGCoordinator, entry: ConfigEntry) -> None:
        CoordinatorEntity.__init__(self, coordinator)
        Camera.__init__(self)
        self._attr_unique_id = f"{entry.entry_id}_camera"
        self._attr_device_info = _device_info(entry)

    @property
    def frame_interval(self) -> float:
        return self.coordinator._grab_interval_ms / 1000.0

    @property
    def is_recording(self) -> bool:
        data = self.coordinator.data
        return bool(data.get("is_recording")) if data else False

    async def async_camera_image(self, width=None, height=None) -> bytes | None:
        return self.coordinator.last_grab_bytes
