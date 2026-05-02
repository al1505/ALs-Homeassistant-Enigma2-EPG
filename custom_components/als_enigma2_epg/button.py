"""Enigma2 EPG Refresh-Button."""
from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
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
    coordinator: Enigma2EPGCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([Enigma2RefreshButton(coordinator, entry)])


class Enigma2RefreshButton(CoordinatorEntity, ButtonEntity):
    """Loest sofortigen EPG-Datenabruf aus."""

    _attr_has_entity_name = True
    _attr_name = "Refresh EPG"
    _attr_icon = "mdi:refresh"
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, coordinator: Enigma2EPGCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_refresh"
        self._attr_device_info = _device_info(entry)

    async def async_press(self) -> None:
        await self.coordinator.async_refresh()
