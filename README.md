# ALs Homeassistant Enigma2 EPG

Home Assistant Custom Integration fuer Enigma2/OpenWebIF Receiver (VU+, Dreambox, u.a.).

[![HACS hinzufuegen](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=al1505&repository=als-enigma2-epg&category=integration)

## Features

- Aktueller Kanal, Sendungsname, Start- und Endzeit
- Lautstaerke, Standby, Aufnahme-Status, Mute
- Picon-URL und Grab-URL fuer die ALs Harmony Companion Card
- Konfigurierbarer Alias-Name und Abrufintervall
- Refresh-Button (Configuration) und Diagnostics (letzter Abruf)

## Installation via HACS

Auf den Badge oben klicken – oder manuell:

1. HACS -> Custom Repositories -> `https://github.com/al1505/als-enigma2-epg` -> Integration
2. Integration installieren und HA neu starten
3. Einstellungen -> Integrationen -> **ALs Homeassistant Enigma2 EPG** hinzufuegen

## Konfiguration

| Feld | Beschreibung |
|---|---|
| IP-Adresse / Hostname | Receiver mit aktiviertem OpenWebIF |
| Port | Standard: 80 |
| HTTPS | Optional |
| Alias | Optionaler Anzeigename |
| Benutzername / Passwort | Optional |
| Aktualisierungsintervall | 10–300 Sekunden (Standard: 30) |

## Voraussetzungen

- Home Assistant 2024.1.0+
- Enigma2-Receiver mit [OpenWebIF](https://github.com/E2OpenPlugins/e2openplugin-OpenWebif)