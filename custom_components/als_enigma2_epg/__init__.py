"""Enigma2 EPG Custom Integration."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .coordinator import Enigma2EPGCoordinator

DOMAIN = "als_enigma2_epg"
PLATFORMS = ["sensor", "binary_sensor", "button", "camera", "media_player"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Integration einrichten: Coordinator starten, Plattformen laden."""
    config = {**entry.data, **entry.options}
    coordinator = Enigma2EPGCoordinator(hass, config)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(_async_update_listener))
    return True


async def _async_update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Coordinator bei Options-Aenderung neu starten (z.B. scan_interval)."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Integration entladen."""
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unloaded:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unloaded
