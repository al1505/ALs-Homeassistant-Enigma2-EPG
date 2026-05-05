"""Config Flow: UI-Konfiguration fuer ALs Enigma2 EPG."""
from __future__ import annotations

import asyncio
import logging

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from . import DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_SCHEMA = vol.Schema(
    {
        vol.Optional("alias", default=""): str,
        vol.Required("host"): str,
        vol.Optional("port", default=80): vol.All(int, vol.Range(min=1, max=65535)),
        vol.Optional("ssl", default=False): bool,
        vol.Optional("username", default=""): str,
        vol.Optional("password", default=""): str,
        vol.Optional("scan_interval", default=30): vol.All(int, vol.Range(min=10, max=300)),
    }
)


async def _test_connection(hass, data: dict) -> str | None:
    """Versucht /api/statusinfo abzurufen. Gibt None bei Erfolg, sonst Fehlercode."""
    scheme = "https" if data.get("ssl") else "http"
    url = f"{scheme}://{data['host']}:{data.get('port', 80)}/api/statusinfo"
    session = async_get_clientsession(hass)

    auth = None
    if data.get("username"):
        from aiohttp import BasicAuth
        auth = BasicAuth(data["username"], data.get("password", ""))

    try:
        async with asyncio.timeout(8):
            async with session.get(url, auth=auth, ssl=data.get("ssl", False)) as resp:
                if resp.status == 401:
                    return "invalid_auth"
                if resp.status != 200:
                    return "cannot_connect"
                return None
    except asyncio.TimeoutError:
        return "timeout"
    except Exception:
        return "cannot_connect"


def _entry_title(data: dict) -> str:
    """Gibt den Anzeigenamen zurueck: Alias wenn gesetzt, sonst Host."""
    return (data.get("alias") or "").strip() or data["host"]


class Enigma2EPGConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Konfigurationsfluss fuer ALs Enigma2 EPG."""

    VERSION = 1

    async def async_step_user(self, user_input: dict | None = None):
        errors: dict[str, str] = {}

        if user_input is not None:
            error = await _test_connection(self.hass, user_input)
            if error:
                errors["base"] = error
            else:
                await self.async_set_unique_id(
                    f"{user_input['host']}:{user_input.get('port', 80)}"
                )
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=_entry_title(user_input),
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_SCHEMA,
            errors=errors,
        )

    @staticmethod
    def async_get_options_flow(config_entry):
        return Enigma2EPGOptionsFlow(config_entry)


class Enigma2EPGOptionsFlow(config_entries.OptionsFlow):
    """Erlaubt nachtraegliche Aenderung von Alias, scan_interval u.a."""

    def __init__(self, entry: config_entries.ConfigEntry) -> None:
        self._entry = entry

    async def async_step_init(self, user_input: dict | None = None):
        if user_input is not None:
            new_title = _entry_title({**self._entry.data, **user_input})
            self.hass.config_entries.async_update_entry(
                self._entry, title=new_title
            )
            return self.async_create_entry(title="", data=user_input)

        schema = vol.Schema(
            {
                vol.Optional(
                    "alias",
                    default=self._entry.data.get("alias", ""),
                ): str,
                vol.Optional(
                    "scan_interval",
                    default=self._entry.options.get(
                        "scan_interval", self._entry.data.get("scan_interval", 30)
                    ),
                ): vol.All(int, vol.Range(min=10, max=300)),
            }
        )
        return self.async_show_form(step_id="init", data_schema=schema)
