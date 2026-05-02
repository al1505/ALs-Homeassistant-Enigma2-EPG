"""Enigma2 EPG Sensor-Entities."""
from __future__ import annotations

from datetime import datetime, timezone

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import DOMAIN
from .coordinator import Enigma2EPGCoordinator

_ATTR_WHITELIST = {
    "currservice_station",
    "currservice_name",
    "currservice_fulldescription",
    "currservice_serviceref",
    "currservice_begin",
    "currservice_end",
    "currservice_begin_timestamp",
    "currservice_end_timestamp",
    "in_standby",
    "is_recording",
    "volume_level",
    "is_volume_muted",
    "enigma2_url",
    "grab_url",
    "picon_url",
    "m3u_url",
    "stream_url",
}


def _device_info(entry: ConfigEntry) -> dict:
    return {
        "identifiers": {(DOMAIN, entry.entry_id)},
        "name": entry.title,
        "manufacturer": "Dream Multimedia / OpenWebIF",
    }


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: Enigma2EPGCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        Enigma2EPGSensor(coordinator, entry),
        Enigma2ProgrammeSensor(coordinator, entry),
        Enigma2StartTimeSensor(coordinator, entry),
        Enigma2EndTimeSensor(coordinator, entry),
        Enigma2RemainingTimeSensor(coordinator, entry),
        Enigma2DescriptionSensor(coordinator, entry),
        Enigma2VolumeSensor(coordinator, entry),
        Enigma2LastUpdateSensor(coordinator, entry),
        Enigma2IPSensor(coordinator, entry),
        Enigma2GrabURLSensor(coordinator, entry),
        Enigma2PiconURLSensor(coordinator, entry),
        Enigma2StreamURLSensor(coordinator, entry),
    ])


class Enigma2EPGSensor(CoordinatorEntity, SensorEntity):
    """Haupt-Sensor: Kanalname + alle EPG-Attribute (benoetigt von der Harmony-Karte)."""

    _attr_icon = "mdi:television-play"
    _attr_has_entity_name = True
    _attr_name = "EPG"

    def __init__(self, coordinator: Enigma2EPGCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_epg"
        self._attr_device_info = _device_info(entry)

    async def async_update(self) -> None:
        """Sofortiger Refresh ohne Debouncer (homeassistant.update_entity)."""
        await self.coordinator.async_refresh()

    @property
    def native_value(self) -> str:
        data = self.coordinator.data
        if not data:
            return "unavailable"
        if data.get("in_standby"):
            return "standby"
        return data.get("currservice_station") or "unknown"

    @property
    def extra_state_attributes(self) -> dict:
        data = self.coordinator.data
        if not data:
            return {}
        return {k: v for k, v in data.items() if k in _ATTR_WHITELIST and v is not None}


class Enigma2ProgrammeSensor(CoordinatorEntity, SensorEntity):
    """Aktueller Sendungsname."""

    _attr_icon = "mdi:text"
    _attr_has_entity_name = True
    _attr_name = "Programme"

    def __init__(self, coordinator: Enigma2EPGCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_programme"
        self._attr_device_info = _device_info(entry)

    @property
    def native_value(self) -> str | None:
        data = self.coordinator.data
        if not data:
            return None
        if data.get("in_standby"):
            return "standby"
        return data.get("currservice_name") or None


class Enigma2StartTimeSensor(CoordinatorEntity, SensorEntity):
    """Startzeit der aktuellen Sendung (HH:MM)."""

    _attr_icon = "mdi:clock-start"
    _attr_has_entity_name = True
    _attr_name = "Start"

    def __init__(self, coordinator: Enigma2EPGCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_start"
        self._attr_device_info = _device_info(entry)

    @property
    def native_value(self) -> str | None:
        data = self.coordinator.data
        if not data:
            return None
        if data.get("in_standby"):
            return "standby"
        return data.get("currservice_begin") or None


class Enigma2EndTimeSensor(CoordinatorEntity, SensorEntity):
    """Endzeit der aktuellen Sendung (HH:MM)."""

    _attr_icon = "mdi:clock-end"
    _attr_has_entity_name = True
    _attr_name = "End"

    def __init__(self, coordinator: Enigma2EPGCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_end"
        self._attr_device_info = _device_info(entry)

    @property
    def native_value(self) -> str | None:
        data = self.coordinator.data
        if not data:
            return None
        if data.get("in_standby"):
            return "standby"
        return data.get("currservice_end") or None


class Enigma2VolumeSensor(CoordinatorEntity, SensorEntity):
    """Lautstaerke in Prozent (0-100)."""

    _attr_icon = "mdi:volume-high"
    _attr_has_entity_name = True
    _attr_name = "Volume"
    _attr_native_unit_of_measurement = "%"

    def __init__(self, coordinator: Enigma2EPGCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_volume"
        self._attr_device_info = _device_info(entry)

    @property
    def native_value(self) -> int | None:
        data = self.coordinator.data
        if not data:
            return None
        vol = data.get("volume_level")
        return round(vol * 100) if vol is not None else None


class Enigma2LastUpdateSensor(CoordinatorEntity, SensorEntity):
    """Zeitpunkt des letzten erfolgreichen Datenabrufs."""

    _attr_icon = "mdi:clock-check"
    _attr_has_entity_name = True
    _attr_name = "Last Update"
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_device_class = SensorDeviceClass.TIMESTAMP

    def __init__(self, coordinator: Enigma2EPGCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_last_update"
        self._attr_device_info = _device_info(entry)

    @property
    def native_value(self):
        return self.coordinator.last_poll_time


class Enigma2IPSensor(CoordinatorEntity, SensorEntity):
    """IP-Adresse des Receivers."""

    _attr_icon = "mdi:ip-network"
    _attr_has_entity_name = True
    _attr_name = "IP Address"

    def __init__(self, coordinator: Enigma2EPGCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_ip"
        self._attr_device_info = _device_info(entry)

    @property
    def native_value(self) -> str:
        return self.coordinator._host


class Enigma2GrabURLSensor(CoordinatorEntity, SensorEntity):
    """Grab-URL fuer TV-Screenshot."""

    _attr_icon = "mdi:camera"
    _attr_has_entity_name = True
    _attr_name = "Grab URL"

    def __init__(self, coordinator: Enigma2EPGCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_grab_url"
        self._attr_device_info = _device_info(entry)

    @property
    def native_value(self) -> str | None:
        data = self.coordinator.data
        return data.get("grab_url") if data else None


class Enigma2PiconURLSensor(CoordinatorEntity, SensorEntity):
    """Picon-URL des aktuellen Kanals."""

    _attr_icon = "mdi:image"
    _attr_has_entity_name = True
    _attr_name = "Picon URL"

    def __init__(self, coordinator: Enigma2EPGCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_picon_url"
        self._attr_device_info = _device_info(entry)

    @property
    def native_value(self) -> str | None:
        data = self.coordinator.data
        if not data:
            return None
        return data.get("picon_url")


class Enigma2StreamURLSensor(CoordinatorEntity, SensorEntity):
    """M3U Stream-URL des aktuellen Kanals (fuer VLC / externe Player)."""

    _attr_icon = "mdi:play-network"
    _attr_has_entity_name = True
    _attr_name = "Stream URL"

    def __init__(self, coordinator: Enigma2EPGCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_stream_url"
        self._attr_device_info = _device_info(entry)

    @property
    def native_value(self) -> str | None:
        data = self.coordinator.data
        if not data:
            return None
        return data.get("m3u_url")


class Enigma2RemainingTimeSensor(CoordinatorEntity, SensorEntity):
    """Verbleibende Zeit bis Sendungsende (H:MM)."""

    _attr_icon = "mdi:timer-outline"
    _attr_has_entity_name = True
    _attr_name = "Remaining Time"

    def __init__(self, coordinator: Enigma2EPGCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_remaining_time"
        self._attr_device_info = _device_info(entry)

    @property
    def native_value(self) -> str | None:
        data = self.coordinator.data
        if not data or data.get("in_standby"):
            return None
        end_ts = data.get("currservice_end_timestamp")
        if not end_ts:
            return None
        try:
            remaining = int(end_ts) - int(datetime.now(timezone.utc).timestamp())
            if remaining <= 0:
                return "0:00"
            h = remaining // 3600
            m = (remaining % 3600) // 60
            return f"{h}:{m:02d}"
        except (ValueError, TypeError):
            return None


class Enigma2DescriptionSensor(CoordinatorEntity, SensorEntity):
    """Beschreibung der aktuellen Sendung."""

    _attr_icon = "mdi:text-long"
    _attr_has_entity_name = True
    _attr_name = "Description"

    def __init__(self, coordinator: Enigma2EPGCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_description"
        self._attr_device_info = _device_info(entry)

    @property
    def native_value(self) -> str | None:
        data = self.coordinator.data
        if not data or data.get("in_standby"):
            return None
        desc = data.get("currservice_fulldescription") or ""
        if not desc:
            return "–"
        # HA-Sensor-State: max 255 Zeichen
        return desc[:255] if len(desc) <= 255 else desc[:252] + "…"
