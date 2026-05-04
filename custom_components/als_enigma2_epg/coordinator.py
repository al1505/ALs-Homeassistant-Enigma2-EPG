"""DataUpdateCoordinator: pollt /api/statusinfo vom OpenWebIF-Receiver."""
from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timedelta, timezone
from typing import Callable
from urllib.parse import quote

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

_LOGGER = logging.getLogger(__name__)

STATUSINFO_PATH = "/api/statusinfo"


class Enigma2EPGCoordinator(DataUpdateCoordinator):
    """Koordiniert den Datenabruf vom Enigma2-Receiver via OpenWebIF."""

    def __init__(self, hass: HomeAssistant, config: dict) -> None:
        self._host = config["host"]
        self._port = int(config.get("port", 80))
        self._ssl = bool(config.get("ssl", False))
        self._username = config.get("username", "")
        self._password = config.get("password", "")
        scheme = "https" if self._ssl else "http"
        self.base_url = f"{scheme}://{self._host}:{self._port}"
        self.last_poll_time: datetime | None = None

        self._grab_interval_ms: int = max(100, int(config.get("grab_interval_ms", 500)))
        self.last_grab_bytes: bytes | None = None
        self.last_grab_hash: str = "0"
        self._grab_counter: int = 0
        self._grab_listeners: list[Callable[[], None]] = []
        self._grab_task: asyncio.Task | None = None

        super().__init__(
            hass,
            _LOGGER,
            name=f"Enigma2 EPG {self._host}",
            update_interval=timedelta(seconds=int(config.get("scan_interval", 30))),
        )

    def start_grab_loop(self, hass: HomeAssistant) -> None:
        """Startet den Hintergrund-Task fuer periodische Grab-Bilder."""
        self._grab_task = hass.async_create_background_task(
            self._grab_loop(), name=f"enigma2_grab_{self._host}"
        )

    def stop_grab_loop(self) -> None:
        """Beendet den Grab-Loop sauber."""
        if self._grab_task and not self._grab_task.done():
            self._grab_task.cancel()

    def add_grab_listener(self, callback: Callable[[], None]) -> None:
        """Registriert Callback, der bei jedem neuen Grab-Frame aufgerufen wird."""
        self._grab_listeners.append(callback)

    async def _grab_loop(self) -> None:
        """Holt Grab-Bilder im konfigurierten Intervall und benachrichtigt Listener."""
        grab_url = self.base_url + "/grab?format=jpg&r=480&mode=video"
        auth = None
        if self._username:
            from aiohttp import BasicAuth
            auth = BasicAuth(self._username, self._password)

        while True:
            if not (self.data and self.data.get("in_standby")):
                try:
                    session = async_get_clientsession(self.hass)
                    async with asyncio.timeout(5.0):
                        async with session.get(grab_url, auth=auth, ssl=self._ssl) as resp:
                            if resp.status == 200:
                                self.last_grab_bytes = await resp.read()
                                self._grab_counter += 1
                                self.last_grab_hash = str(self._grab_counter)
                                for cb in self._grab_listeners:
                                    cb()
                except asyncio.CancelledError:
                    return
                except Exception as err:
                    _LOGGER.debug("Grab-Loop Fehler: %s", err)
            try:
                await asyncio.sleep(self._grab_interval_ms / 1000.0)
            except asyncio.CancelledError:
                return

    async def _async_update_data(self) -> dict:
        """Ruft /api/statusinfo ab und gibt die geparsten Daten zurueck."""
        url = self.base_url + STATUSINFO_PATH
        session = async_get_clientsession(self.hass)

        auth = None
        if self._username:
            from aiohttp import BasicAuth
            auth = BasicAuth(self._username, self._password)

        try:
            async with asyncio.timeout(10):
                async with session.get(url, auth=auth, ssl=self._ssl) as resp:
                    if resp.status != 200:
                        raise UpdateFailed(f"HTTP {resp.status} von {url}")
                    raw = await resp.json(content_type=None)
        except asyncio.TimeoutError as err:
            raise UpdateFailed(f"Timeout beim Abruf von {url}") from err
        except Exception as err:
            raise UpdateFailed(f"Verbindungsfehler: {err}") from err

        self.last_poll_time = datetime.now(timezone.utc)
        return self._parse(raw)

    def _parse(self, raw: dict) -> dict:
        """Normalisiert die OpenWebIF-Antwort und ergaenzt abgeleitete Felder."""
        station = (raw.get("currservice_station") or "").strip()

        return {
            "currservice_station":         station,
            "currservice_name":            (raw.get("currservice_name") or "").strip(),
            "currservice_fulldescription": (raw.get("currservice_fulldescription") or "").strip(),
            "currservice_serviceref":      raw.get("currservice_serviceref", ""),
            "currservice_begin":           raw.get("currservice_begin", ""),
            "currservice_end":             raw.get("currservice_end", ""),
            "currservice_begin_timestamp": raw.get("currservice_begin_timestamp"),
            "currservice_end_timestamp":   raw.get("currservice_end_timestamp"),
            "in_standby":    self._to_bool(raw.get("inStandby", False)),
            "is_recording":  self._to_bool(raw.get("isRecording", False)),
            "is_streaming":  self._to_bool(raw.get("isStreaming", False)),
            "volume_level":  self._norm_volume(raw.get("volume")),
            "is_volume_muted": self._to_bool(raw.get("muted", False)),
            "enigma2_url": self.base_url,
            "grab_url":    self.base_url + "/grab?format=jpg&r=480&mode=video",
            "picon_url":   (self.base_url + "/picon/" + quote(station) + ".png") if station else None,
            "m3u_url":     (self.base_url + "/web/stream.m3u?ref=" + quote(raw.get("currservice_serviceref", "")))
                           if raw.get("currservice_serviceref") else None,
            "stream_url":  (f"http://{self._host}:8001/" + raw.get("currservice_serviceref", ""))
                           if raw.get("currservice_serviceref") else None,
        }

    @staticmethod
    def _to_bool(val) -> bool:
        """OpenWebIF liefert booleans manchmal als String 'true'/'false'."""
        if isinstance(val, bool):
            return val
        if isinstance(val, str):
            return val.lower() not in ("false", "0", "")
        return bool(val)

    @staticmethod
    def _norm_volume(raw_vol) -> float | None:
        if raw_vol is None:
            return None
        try:
            return max(0.0, min(1.0, int(raw_vol) / 100.0))
        except (ValueError, TypeError):
            return None
