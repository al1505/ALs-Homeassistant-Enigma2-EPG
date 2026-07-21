# HACS-Audit — 2026-07-21

Vollständige Prüfung aller HA-Projekte mit Git-Environment und aktivem HACS-Reporting (`hacs.json` + öffentlicher GitHub-Remote), ausgelöst durch @frenck's Review-Kommentar auf PR [hacs/default#7381](https://github.com/hacs/default/pull/7381) (fehlende `LICENSE`).

Quellen: offizielle HACS-Docs ([Start](https://www.hacs.xyz/docs/publish/start/), [Integration](https://www.hacs.xyz/docs/publish/integration/), [Plugin](https://www.hacs.xyz/docs/publish/plugin/)) + HA Dev Docs zu Brand-Assets (Stand HA ≥2026.3: Brand-Icons liegen inline unter `custom_components/<domain>/brand/icon.png`, nicht mehr im separaten `home-assistant/brands`-Repo).

## Geprüfte Projekte

Von 12 Ordnern unter `H:\Home-Assistant\` erfüllen 4 beide Kriterien (Git-Repo + `hacs.json` + öffentlicher Remote):

| Projekt | Typ | HACS-Default-PR |
|---|---|---|
| ALs-Homeassistant-Enigma2-EPG | Integration | [#7381](https://github.com/hacs/default/pull/7381) |
| ALs-HA-SundanceMarin | Integration | *(kein offener PR gefunden — noch nicht bei hacs/default eingereicht)* |
| ALs-Homeassistant-Harmony-Companion-Card | Plugin/Card | [#7383](https://github.com/hacs/default/pull/7383) |
| ALs-Homeassitant-Energiebilanz-Card | Plugin/Card | [#7382](https://github.com/hacs/default/pull/7382) |

Alle 4 haben `manifest.json`/`hacs.json` vollständig, öffentliche Repos mit Description + Topics, GitHub erkennt die Lizenz korrekt (`mit`), CI (`validate`/`hassfest`) ist grün.

## Befund: LICENSE fehlte im ausgelieferten Release

Bei allen 4 Projekten war `LICENSE` zwar committed, aber **nach** dem jeweils letzten GitHub-Release hinzugefügt worden — HACS installiert aus dem Release-Tarball, nicht von `main`. Per GitHub-API bestätigt (404 auf `LICENSE` im alten Release-Tag).

### Fix — neue Releases geschnitten

| Projekt | Alter Release (ohne LICENSE) | Neuer Release (mit LICENSE, verifiziert) |
|---|---|---|
| Enigma2-EPG | v1.7.1 (2026-05-05) | **v1.7.2** |
| SundanceMarin | v1.4.0 (2026-06-22) | **v1.5.4** (enthielt bereits unveröffentlichte Fixes 1.4.1–1.5.4) |
| Harmony-Companion-Card | v5.5.1 (2026-05-14) | **v5.5.2** |
| Energiebilanz-Card | v1.0.1 (2026-05-02) | **v4.6.0** (Code stand schon auf 4.6.0, nie released; toter Draft-Release "v4.6" von März wurde gelöscht) |

Verifikation: `gh api repos/al1505/<repo>/contents/LICENSE?ref=<tag>` liefert für alle 4 neuen Tags `200 OK`.

### Nebenbefund: CRLF-Korruption durch Edit-Tool

Beim Versions-Bump hat das Editor-Tool zweimal (`manifest.json` bei Enigma2-EPG, `harmony-companion-card.js` bei Harmony) die komplette Datei versehentlich auf CRLF umgestellt statt nur eine Zeile zu ändern (8700-Zeilen-Diff für eine Versionsnummer). Funktional harmlos (JSON/JS-Parser ignorieren das), aber inkonsistent mit dem Rest des jeweiligen Repos (überall sonst LF, `core.autocrlf=false`, kein `.gitattributes`). Per Python-Byte-Replace (`\r\n` → `\n`) zurück auf LF normalisiert und nachcorrigiert:

- Enigma2-EPG: zusätzlicher Release **v1.7.2** (statt v1.7.1)
- Harmony-Companion-Card: im selben Commit wie der Versions-Bump auf **v5.5.2** mitgefixt

**Wichtig für künftige Sessions:** Bei Versions-Bumps in JSON/JS-Dateien in diesem Windows-Environment nach dem Edit `git diff --stat` prüfen — wenn die Zeilenzahl der Änderung die Dateigröße übersteigt, ist das ein CRLF-Bug, nicht ein echter inhaltlicher Unterschied. Notfalls Python-Byte-Replace statt Edit-Tool für reine Ein-Zeilen-Änderungen in bestehenden Dateien nutzen.

## Offene, vom LICENSE-Fix unabhängige Befunde

### 1. PRs #7382 (Energiebilanz-Card) und #7383 (Harmony-Companion-Card) sind strukturell kaputt

Beide PRs ändern **zwei** Katalogdateien (`integration` **und** `plugin`) statt nur `plugin`, und **beide Diffs sind massiv aufgebläht** (`integration`: +2266/-2265 Zeilen, `plugin`: +580/-579 Zeilen) — exakt dasselbe Line-Ending-Korruptions-Muster, das frenck bei Enigma2-EPG in der ersten Review (siehe unten) bereits bemängelt hat. `hacs-bot` hat automatisiert schon "Limit your PR to a single file change" kommentiert. Diese beiden PRs sind **nicht** durch den LICENSE-Fix gelöst — sie brauchen einen sauberen Branch-Reset auf aktuellen `hacs/default`-master + Ein-Zeilen-Add in der `plugin`-Datei, analog zu dem, was für Enigma2-EPG (PR #7381) bereits erledigt wurde (siehe frenck's erste Review dort).

**Diese Reparatur wurde in dieser Session noch nicht durchgeführt** — nur der LICENSE-Fix in den Quell-Repos selbst.

### 2. Harmony-Companion-Card liefert `harmony-card-v2.js` nicht aus

README dokumentiert zwei Karten (`custom:harmony-companion-card` und `custom:harmony-card-v2`), aber `hacs.json` deklariert per `"filename"` nur die erste Datei. Laut HACS-Doku lädt HACS bei gesetztem `filename` **ausschließlich** diese eine Datei — `harmony-card-v2.js` wird nie an HACS-Nutzer ausgeliefert. Lösung vermutlich: beide Dateien in ein `dist/`-Verzeichnis bündeln und `filename` aus `hacs.json` entfernen (HACS lädt dann alle `.js` aus `dist/`). Nicht umgesetzt — struktureller Eingriff, kein reiner Release-Fix.

### 3. Enigma2-EPG: doppelte Icon-Dateien

`custom_components/als_enigma2_epg/icon.png` + `icon@2x.png` liegen sowohl im Integration-Root als auch (korrekt) unter `brand/`. Die Root-Kopien sind vermutlich Altlasten vor der Umstellung auf den neuen inline-Brand-Mechanismus (HA ≥2026.3). Kein HACS-Blocker, nur unnötige Duplikate.

### 4. SundanceMarin: nicht bei hacs/default eingereicht

Kein offener PR gefunden. Falls die Aufnahme in den Default-Store gewünscht ist, fehlt noch der Submission-PR.

## Status der HACS-Default-PRs (Stand 2026-07-21)

| PR | reviewDecision | isDraft | Nächster Schritt |
|---|---|---|---|
| [#7381](https://github.com/hacs/default/pull/7381) Enigma2-EPG | CHANGES_REQUESTED (Label stale, wird bei nächster Review von frenck aktualisiert) | **false** | Erledigt: LICENSE (v1.7.2), Branch-Reset auf aktuellen `hacs/default:master` (war `BEHIND`, mehrere andere Katalogeinträge wurden zwischenzeitlich entfernt), sauberer `+1/-0`-Diff, "Ready for review" gesetzt. Wartet jetzt auf frenck. |
| [#7382](https://github.com/hacs/default/pull/7382) Energiebilanz-Card | CHANGES_REQUESTED (Label stale) | **false** | Erledigt: sauberer `+1/-0`-Diff in `plugin` (statt kaputtem Doppel-Datei-Diff), "Ready for review" gesetzt. Wartet auf Review. |
| [#7383](https://github.com/hacs/default/pull/7383) Harmony-Companion-Card | CHANGES_REQUESTED (Label stale) | **false** | Erledigt: sauberer `+1/-0`-Diff in `plugin` (statt kaputtem Doppel-Datei-Diff), "Ready for review" gesetzt. Wartet auf Review. |

### Nachtrag: Branch-Update PR #7381 (2026-07-21, nach hacs-bot "branch out of date")

Der Fork-Branch `al1505/default:add-als-enigma2-epg-v2` war `BEHIND` `hacs/default:master` (enthielt zudem noch einen alten Merge-Commit aus der ersten Review-Runde). Fix: neuer Branch direkt von `upstream/master` erstellt, die eine Zeile `"al1505/ALs-Homeassistant-Enigma2-EPG"` an der korrekten sortierten Stelle eingefügt (zwischen `al-one/hass-xiaomi-miot` und `alakdae/AquastillaHA`), verifiziert (`git diff --stat` = exakt `+1/-0`, kein CRLF), und mit `git push --force-with-lease` auf den PR-Branch geschoben. `mergeStateStatus` danach `BLOCKED` (normal, wartet auf Review) statt `BEHIND`. Anschließend `gh pr ready 7381 -R hacs/default` ausgeführt.

### Nachtrag: PRs #7382 + #7383 nach demselben Verfahren repariert (2026-07-21)

Beide PRs hatten den in Befund 1 beschriebenen Doppel-Datei-Diff (`integration` +2266/-2265 UND `plugin` +580/-579). Fix: jeweils neuer Branch von `upstream/master`, nur die eigene Zeile in `plugin` eingefügt — Sortierposition mit `hacs/default`s eigenem `scripts/is_sorted.py` verifiziert (Katalog wird **case-insensitive** sortiert, `sorted(content, key=str.casefold)`, nicht simple ASCII-Sortierung — beide Einträge gehören zwischen `aex351/home-assistant-neerslag-card` und `alex-taylor/energy-distribution-ext`). `integration` wurde in keinem der beiden Branches mehr angefasst. Beide mit `--force-with-lease` gepusht und auf "Ready for review" gesetzt.

**Wichtig fürs nächste Mal:** `hacs/default` sortiert case-insensitive (`str.casefold`), nicht nach roher Byte-Reihenfolge — bei künftigen Katalog-Einträgen immer `scripts/is_sorted.py` im Ziel-Repo konsultieren statt die Position zu erraten.
