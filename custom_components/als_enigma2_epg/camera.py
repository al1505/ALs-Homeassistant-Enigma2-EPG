"""Enigma2 EPG Camera – zeigt aktuelles TV-Bild via Grab-URL (HA-proxied)."""
from __future__ import annotations
import asyncio
import logging
from homeassistant.components.camera import Camera, CameraEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from . import DOMAIN
from .coordinator import Enigma2EPGCoordinator
from .sensor import _device_info

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([Enigma2Camera(coordinator, entry)])

class Enigma2Camera(CoordinatorEntity, Camera):
    _attr_has_entity_name = True
    _attr_name = "TV"
    _attr_icon = "mdi:television-play"
    _attr_supported_features = CameraEntityFeature.STREAM

    def __init__(self, coordinator, entry):
        CoordinatorEntity.__init__(self, coordinator)
        Camera.__init__(self)
        self._attr_unique_id = f"{entry.entry_id}_camera"
        self._attr_device_info = _device_info(entry)

    @property
    def is_recording(self):
        data = self.coordinator.data
        return bool(data.get("is_recording")) if data else False

    async def stream_source(self) -> str | None:
        data = self.coordinator.data
        if not data or data.get("in_standby"):
            return None
        return data.get("stream_url")

    async def async_camera_image(self, width=None, height=None):
        data = self.coordinator.data
        if not data or data.get("in_standby"):
            return None
        grab_url = data.get("grab_url")
        if not grab_url:
            return None
        auth = None
        if self.coordinator._username:
            from aiohttp import BasicAuth
            auth = BasicAuth(self.coordinator._username, self.coordinator._password)
        session = async_get_clientsession(self.hass)
        try:
            async with asyncio.timeout(10):
                async with session.get(grab_url, auth=auth, ssl=self.coordinator._ssl) as resp:
                    if resp.status == 200:
                        return await resp.read()
        except Exception as err:
            _LOGGER.debug("Grab-URL Fehler: %s", err)
        return None
