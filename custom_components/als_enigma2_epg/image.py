"""Enigma2 EPG Image – Picon und Grab-Screenshot als HA Image-Entities."""
from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timezone

from homeassistant.components.image import ImageEntity
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
    async_add_entities([
        Enigma2PiconImage(coordinator, entry),
        Enigma2GrabImage(coordinator, entry),
    ])


class Enigma2PiconImage(CoordinatorEntity, ImageEntity):
    _attr_has_entity_name = True
    _attr_name = "Picon"
    _attr_icon = "mdi:television-classic"
    _attr_content_type = "image/png"

    def __init__(self, coordinator: Enigma2EPGCoordinator, entry: ConfigEntry) -> None:
        CoordinatorEntity.__init__(self, coordinator)
        ImageEntity.__init__(self, coordinator.hass)
        self._attr_unique_id = f"{entry.entry_id}_picon"
        self._attr_device_info = _device_info(entry)
        self._attr_image_last_updated = datetime.now(timezone.utc)
        self._current_picon_url: str | None = None

    def _handle_coordinator_update(self) -> None:
        """image_last_updated aktualisieren wenn Kanal gewechselt hat."""
        data = self.coordinator.data
        new_url = data.get("picon_url") if data else None
        if new_url != self._current_picon_url:
            self._current_picon_url = new_url
            self._attr_image_last_updated = datetime.now(timezone.utc)
        super()._handle_coordinator_update()

    async def async_image(self) -> bytes | None:
        data = self.coordinator.data
        if not data or data.get("in_standby"):
            return None
        picon_url = data.get("picon_url")
        if not picon_url:
            return None
        auth = None
        if self.coordinator._username:
            from aiohttp import BasicAuth
            auth = BasicAuth(self.coordinator._username, self.coordinator._password)
        session = async_get_clientsession(self.hass)
        try:
            async with asyncio.timeout(10):
                async with session.get(picon_url, auth=auth, ssl=self.coordinator._ssl) as resp:
                    if resp.status == 200:
                        return await resp.read()
        except Exception as err:
            _LOGGER.debug("Picon-Abruf fehlgeschlagen: %s", err)
        return None


class Enigma2GrabImage(CoordinatorEntity, ImageEntity):
    _attr_has_entity_name = True
    _attr_name = "Grab"
    _attr_icon = "mdi:television-play"
    _attr_content_type = "image/jpeg"

    def __init__(self, coordinator: Enigma2EPGCoordinator, entry: ConfigEntry) -> None:
        CoordinatorEntity.__init__(self, coordinator)
        ImageEntity.__init__(self, coordinator.hass)
        self._attr_unique_id = f"{entry.entry_id}_grab"
        self._attr_device_info = _device_info(entry)
        self._attr_image_last_updated = datetime.now(timezone.utc)

    def _handle_coordinator_update(self) -> None:
        """Bei jedem Poll image_last_updated setzen damit HA das Bild neu laedt."""
        if self.coordinator.data and not self.coordinator.data.get("in_standby"):
            self._attr_image_last_updated = datetime.now(timezone.utc)
        super()._handle_coordinator_update()

    async def async_image(self) -> bytes | None:
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
            _LOGGER.debug("Grab-Abruf fehlgeschlagen: %s", err)
        return None
