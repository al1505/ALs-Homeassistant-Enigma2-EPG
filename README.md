# ALs Homeassistant Enigma2 EPG

[![HACS Custom](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://hacs.xyz)
[![GitHub Release](https://img.shields.io/github/v/release/al1505/ALs-Homeassistant-Enigma2-EPG?label=Version)](https://github.com/al1505/ALs-Homeassistant-Enigma2-EPG/releases)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PayPal](https://img.shields.io/badge/PayPal-Donate-0070ba?logo=paypal&style=flat-square)](https://paypal.me/al1505)

[![HACS hinzufuegen](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=al1505&repository=als-enigma2-epg&category=integration)

[🇩🇪 Deutsch](#deutsch) | [🇬🇧 English](#english)

---

## Deutsch

> Home Assistant Custom Integration fuer Enigma2/OpenWebIF Receiver (VU+, Dreambox, u.a.).
> Liefert EPG-Daten, Senderlogo (Picon), Lautstaerke-Anzeige und mehr — optimal kombiniert mit der [ALs Harmony Companion Card](https://github.com/al1505/ALs-Homeassistant-Harmony-Companion-Card).

---

## ☕ Support

Wenn dir diese Integration gefaellt und du die Weiterentwicklung unterstuetzen moechtest:

[![Buy me a coffee](https://img.shields.io/badge/Buy%20me%20a%20coffee-PayPal-0070ba?logo=paypal&style=for-the-badge)](https://paypal.me/al1505)

Direkt-Link: **[paypal.me/al1505](https://paypal.me/al1505)** ❤️

---

## ✨ Features

- Aktueller Kanal, Sendungsname, Start- und Endzeit, verbleibende Zeit
- EPG-Beschreibung der laufenden Sendung
- **Picon (Senderlogo)** als natives HA Image-Entity — aktualisiert sich automatisch bei Kanalwechsel
- Picon-URL und Grab-URL fuer die ALs Harmony Companion Card
- Lautstaerke-Anzeige (%), Mute-, Standby- und Aufnahme-Status (read-only Sensoren)
- Konfigurierbarer Alias-Name und Abrufintervall
- Refresh-Button und Diagnostics (letzter Abruf)

## Installation via HACS

Auf den Badge oben klicken – oder manuell:

1. HACS → Custom Repositories → `https://github.com/al1505/als-enigma2-epg` → Integration
2. Integration installieren und HA neu starten
3. Einstellungen → Integrationen → **ALs Homeassistant Enigma2 EPG** hinzufuegen

## Konfiguration

### Ersteinrichtung

| Feld | Beschreibung |
|---|---|
| IP-Adresse / Hostname | Receiver mit aktiviertem OpenWebIF |
| Port | Standard: 80 |
| HTTPS | Optional |
| Alias | Optionaler Anzeigename |
| Benutzername / Passwort | Optional |
| Aktualisierungsintervall | 10–300 Sekunden (Standard: 30) |

### Einstellungen nachtraeglich aendern

**Einstellungen → Geraete & Dienste → ALs Homeassistant Enigma2 EPG → Drei-Punkte-Menü → Konfigurieren**

## Entities

| Entity | Typ | Beschreibung |
|---|---|---|
| EPG | Sensor | Kanalname + alle EPG-Attribute als State-Attribute |
| Programme | Sensor | Sendungsname |
| Start / End | Sensor | Start- und Endzeit (HH:MM) |
| Remaining Time | Sensor | Verbleibende Zeit bis Sendungsende |
| Description | Sensor | EPG-Langbeschreibung |
| Volume | Sensor | Lautstaerke in % |
| Grab URL | Sensor | Screenshot-URL (Attribut: `url`) |
| Picon URL | Sensor | Senderlogo-URL (Attribut: `url`) |
| Stream URL | Sensor | M3U Stream-URL (Attribut: `url`) |
| IP Address | Sensor | IP-Adresse des Receivers |
| Last Update | Sensor (Diagnostics) | Zeitpunkt des letzten Datenabrufs |
| Standby | Binary Sensor | Receiver im Standby |
| Recording | Binary Sensor | Aufnahme laeuft |
| Muted | Binary Sensor | Ton stummgeschaltet |
| Picon | Image | Senderlogo – aktualisiert sich bei Kanalwechsel |
| Grab | Image | TV-Screenshot – aktualisiert sich im Abrufintervall |
| Refresh EPG | Button (Configuration) | Sofortiger manueller Datenabruf |

## Voraussetzungen

- Home Assistant 2024.1.0+
- Enigma2-Receiver mit [OpenWebIF](https://github.com/E2OpenPlugins/e2openplugin-OpenWebif)

## Lizenz

MIT License

---

[![Buy me a coffee](https://img.shields.io/badge/Buy%20me%20a%20coffee-PayPal-0070ba?logo=paypal&style=for-the-badge)](https://paypal.me/al1505)

**[paypal.me/al1505](https://paypal.me/al1505)** ☕

---

## English

> Home Assistant custom integration for Enigma2/OpenWebIF receivers (VU+, Dreambox, and others).
> Provides EPG data, channel logo (Picon), volume display, and more — pairs perfectly with the [ALs Harmony Companion Card](https://github.com/al1505/ALs-Homeassistant-Harmony-Companion-Card).

---

## ☕ Support

If you like this integration and want to support its ongoing development:

[![Buy me a coffee](https://img.shields.io/badge/Buy%20me%20a%20coffee-PayPal-0070ba?logo=paypal&style=for-the-badge)](https://paypal.me/al1505)

Direct link: **[paypal.me/al1505](https://paypal.me/al1505)** ❤️

---

## ✨ Features

- Current channel, programme name, start and end time, remaining time
- EPG description of the currently running programme
- **Picon (channel logo)** as a native HA image entity — updates automatically on channel change
- Picon URL and grab URL for the ALs Harmony Companion Card
- Volume display (%), mute, standby, and recording status (read-only sensors)
- Configurable alias name and polling interval
- Refresh button and diagnostics (last update)

## Installation via HACS

Click the badge above – or install manually:

1. HACS → Custom Repositories → `https://github.com/al1505/als-enigma2-epg` → Integration
2. Install the integration and restart Home Assistant
3. Settings → Integrations → add **ALs Homeassistant Enigma2 EPG**

## Configuration

### Initial setup

| Field | Description |
|---|---|
| IP address / hostname | Receiver with OpenWebIF enabled |
| Port | Default: 80 |
| HTTPS | Optional |
| Alias | Optional display name |
| Username / password | Optional |
| Update interval | 10–300 seconds (default: 30) |

### Changing settings later

**Settings → Devices & Services → ALs Homeassistant Enigma2 EPG → three-dot menu → Configure**

## Entities

| Entity | Type | Description |
|---|---|---|
| EPG | Sensor | Channel name + all EPG attributes as state attributes |
| Programme | Sensor | Programme name |
| Start / End | Sensor | Start and end time (HH:MM) |
| Remaining Time | Sensor | Time remaining until the programme ends |
| Description | Sensor | Long EPG description |
| Volume | Sensor | Volume in % |
| Grab URL | Sensor | Screenshot URL (attribute: `url`) |
| Picon URL | Sensor | Channel logo URL (attribute: `url`) |
| Stream URL | Sensor | M3U stream URL (attribute: `url`) |
| IP Address | Sensor | IP address of the receiver |
| Last Update | Sensor (Diagnostics) | Timestamp of the last data fetch |
| Standby | Binary Sensor | Receiver is in standby |
| Recording | Binary Sensor | Recording in progress |
| Muted | Binary Sensor | Audio is muted |
| Picon | Image | Channel logo – updates on channel change |
| Grab | Image | TV screenshot – updates at the polling interval |
| Refresh EPG | Button (Configuration) | Triggers an immediate manual data fetch |

## Requirements

- Home Assistant 2024.1.0+
- Enigma2 receiver with [OpenWebIF](https://github.com/E2OpenPlugins/e2openplugin-OpenWebif)

## License

MIT License

---

[![Buy me a coffee](https://img.shields.io/badge/Buy%20me%20a%20coffee-PayPal-0070ba?logo=paypal&style=for-the-badge)](https://paypal.me/al1505)

**[paypal.me/al1505](https://paypal.me/al1505)** ☕
