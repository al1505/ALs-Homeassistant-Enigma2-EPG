"""Enigma2 EPG Media Player – Steuerung + Bild via Grab-Cache."""
from __future__ import annotations

import asyncio
import logging

from homeassistant.components.media_player import (
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
    MediaPlayerState,
    MediaType,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import DOMAIN
from .coordinator import Enigma2EPGCoordinator
from .sensor import _device_info

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([Enigma2MediaPlayer(coordinator, entry)])


class Enigma2MediaPlayer(CoordinatorEntity, MediaPlayerEntity):
    _attr_has_entity_name = True
    _attr_name = "Player"
    _attr_media_content_type = MediaType.TVSHOW
    _attr_supported_features = (
        MediaPlayerEntityFeature.VOLUME_SET
        | MediaPlayerEntityFeature.VOLUME_MUTE
        | MediaPlayerEntityFeature.VOLUME_STEP
    )

    def __init__(self, coordinator: Enigma2EPGCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_mediaplayer"
        self._attr_device_info = _device_info(entry)

    @property
    def media_image_hash(self) -> str:
        # Aendert sich beim Coordinator-Poll (30s) – kein Rapid-Refresh um state_changed-Spam zu vermeiden
        return self.coordinator.last_grab_hash

    async def async_get_media_image(self) -> tuple[bytes | None, str | None]:
        image = self.coordinator.last_grab_bytes
        if image:
            return (image, "image/jpeg")
        return (None, None)

    @property
    def state(self) -> MediaPlayerState:
        data = self.coordinator.data
        if not data:
            return MediaPlayerState.OFF
        if data.get("in_standby"):
            return MediaPlayerState.IDLE
        return MediaPlayerState.PLAYING

    @property
    def media_title(self) -> str | None:
        data = self.coordinator.data
        return data.get("currservice_name") if data else None

    @property
    def media_channel(self) -> str | None:
        data = self.coordinator.data
        return data.get("currservice_station") if data else None

    @property
    def media_series_title(self) -> str | None:
        return self.media_channel

    @property
    def media_artist(self) -> str | None:
        """EPG-Beschreibung als sichtbare Textzeile im Media-Player-Card."""
        data = self.coordinator.data
        if not data or data.get("in_standby"):
            return None
        return data.get("currservice_fulldescription") or None

    @property
    def volume_level(self) -> float | None:
        data = self.coordinator.data
        return data.get("volume_level") if data else None

    @property
    def is_volume_muted(self) -> bool | None:
        data = self.coordinator.data
        return bool(data.get("is_volume_muted")) if data else None

    @property
    def extra_state_attributes(self) -> dict:
        data = self.coordinator.data
        if not data:
            return {}
        attrs = {}
        if data.get("currservice_fulldescription"):
            attrs["description"] = data["currservice_fulldescription"]
        if data.get("currservice_begin"):
            attrs["start"] = data["currservice_begin"]
        if data.get("currservice_end"):
            attrs["end"] = data["currservice_end"]
        return attrs

    async def _api_call(self, path: str) -> None:
        auth = None
        if self.coordinator._username:
            from aiohttp import BasicAuth
            auth = BasicAuth(self.coordinator._username, self.coordinator._password)
        url = self.coordinator.base_url + path
        session = async_get_clientsession(self.hass)
        try:
            async with asyncio.timeout(5):
                await session.get(url, auth=auth, ssl=self.coordinator._ssl)
        except Exception as err:
            _LOGGER.warning("API-Aufruf fehlgeschlagen %s: %s", path, err)

    async def async_set_volume_level(self, volume: float) -> None:
        vol_int = max(0, min(100, int(volume * 100)))
        await self._api_call(f"/api/vol?set=set{vol_int}")
        await self.coordinator.async_refresh()

    async def async_mute_volume(self, mute: bool) -> None:
        await self._api_call("/api/vol?set=mute")
        await self.coordinator.async_refresh()

    async def async_volume_up(self) -> None:
        await self._api_call("/api/vol?set=up")
        await self.coordinator.async_refresh()

    async def async_volume_down(self) -> None:
        await self._api_call("/api/vol?set=down")
        await self.coordinator.async_refresh()
