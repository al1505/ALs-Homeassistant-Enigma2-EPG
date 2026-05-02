# ALs Enigma2 EPG

Home Assistant Custom Integration fuer Enigma2/OpenWebIF Receiver (VU+, Dreambox, u.a.).

## Features

- Aktueller Kanal, Sendungsname, Start- und Endzeit
- Lautstaerke, Standby, Aufnahme-Status, Mute
- Picon-URL und Grab-URL fuer die ALs Harmony Companion Card
- Konfigurierbarer Alias-Name und Abrufintervall
- Refresh-Button und Diagnostics (letzter Abruf)

## Installation via HACS

1. HACS -> Custom Repositories -> `https://github.com/al1505/als-enigma2-epg` -> Integration
2. Integration installieren
3. HA neu starten
4. Einstellungen -> Integrationen -> ALs Enigma2 EPG hinzufuegen

## Konfiguration

- **IP-Adresse / Hostname** des Receivers mit aktiviertem OpenWebIF
- **Port** (Standard: 80)
- **Alias** (optionaler Anzeigename)
- **Benutzername / Passwort** (optional)
- **Aktualisierungsintervall** (10-300 Sekunden, Standard: 30)

## Voraussetzungen

- Home Assistant 2024.1.0+
- Enigma2-Receiver mit [OpenWebIF](https://github.com/E2OpenPlugins/e2openplugin-OpenWebif)